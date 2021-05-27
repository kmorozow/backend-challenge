"""Flask app factory."""
from typing import List, Union, Tuple

from flask import Flask, jsonify, request
from sqlalchemy import func
from sqlalchemy.orm import aliased

from app.models import Artist, db, Metric


def create_app(config_class: object):
    """Create Flask app.

    Args:
        config_class: configuation for Flask app
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    @app.route("/ping", methods=["GET", "POST"])
    def ping() -> str:
        """Return string to show the server is alive."""
        return "Server is here"

    @app.route("/metrics", methods=["GET"])
    def metrics() -> Union[List, Tuple]:
        metric_value = request.args.get("metric_value", type=int)
        if not metric_value:
            return "bad or missing argument", 400

        # There is no standard way to find day difference in sql,
        # so window function used
        subquery = db.session.query(
            Metric,
            func.rank().over(
                order_by=Metric.date.asc(),
                partition_by=Metric.artist_id
            ).label('rank')
        ).subquery()
        prev_day = aliased(subquery)
        res = db.session.query(subquery).\
            with_entities(subquery.c.artist_id, subquery.c.date).\
            join(prev_day,
                 (subquery.c.artist_id == prev_day.c.artist_id) &
                 (subquery.c.rank - prev_day.c.rank == 1)
                 ).\
            where((subquery.c.value >= metric_value) &
                  (prev_day.c.value < metric_value)
                  )

        # Add all artist ids
        artist_crosses = {artist.id: [] for artist in Artist.query.all()}
        for artist_id, date in res.all():
            artist_crosses[artist_id].append(date.isoformat())
        artist_crosses_resp = [{"artist_id": artist_id, "crossings": cross}
                               for artist_id, cross in artist_crosses.items()]
        return jsonify(artist_crosses_resp)

    return app

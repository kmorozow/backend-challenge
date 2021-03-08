"""Unit tests."""

import unittest
import datetime

from app.config import TestingConfig
from app import create_app, db

from app.models.models import Artist, Metric


class TestSetup(unittest.TestCase):
    """Unit testing setup."""

    def setUp(self):
        """Create new app and database for each test."""
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Remove databse and app context after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class TestBasic(TestSetup):
    """Basic default tests."""

    def test_ping(self):
        """Test that app can be pinged wth GET and POST."""
        response = self.app.test_client().get("/ping")
        self.assertEqual(response.status_code, 200)
        response = self.app.test_client().post("/ping")
        self.assertEqual(response.status_code, 200)


class TestMetrics(TestSetup):
    """Test metrics route."""

    def test_route(self):
        # Create data
        for i in range(100):
            db.session.add(Artist())
            for j in range(1000):
                date = datetime.date.today() - datetime.timedelta(j)
                value = (1000 - j) / (i + 1)
                db.session.add(Metric(artist_id=i+1, date=date, value=value))
        db.session.commit()

        # Call endpoint and record performance
        start_time = datetime.datetime.now()
        response = self.app.test_client().get("/metrics?metric_value=50")
        end_time = datetime.datetime.now()
        duration = (end_time - start_time)
        print(f"Response time: {duration.total_seconds()}")

        # Test response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 100)
        self.assertEqual(response.json[0]["artist_id"], 1)
        self.assertEqual(
            response.json[0]["crossings"][0],
            (datetime.date.today() - datetime.timedelta(950)).strftime("%Y-%m-%d")
        )

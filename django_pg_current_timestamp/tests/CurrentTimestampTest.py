# -*- coding: utf-8 -*-

from django.test import TestCase
from django.utils import timezone

from django_pg_current_timestamp.django_pg_current_timestamp_test_app.models import TestModel
import django_pg_current_timestamp


class CurrentTimestampTest(TestCase):

    def setUp(self):
        django_pg_current_timestamp.init()

    def testCurrentTimestamp(self):
        a = TestModel.objects.create(value='altavista.com')
        b = TestModel.objects.get(id=a.id)

        # These shouldn't match, because the TS returned with the initial object is app-generated, whereas the queried object `b` should have the database's `CURRENT_TIMESTAMP` value.
        self.assertNotEqual(a.created_ts, b.created_ts)
        self.assertNotEqual(a.modified_ts, b.modified_ts)

        # These should match if the object was created using `CURRENT_TIMESTAMP`.
        self.assertEqual(b.created_ts, b.modified_ts)
        self.assertEqual(b.created_ts, b.modified_ts)

        b.value='scala.sh'
        b.save()
        c = TestModel.objects.get(id=a.id)

        self.assertNotEqual(b.modified_ts, c.modified_ts)
        self.assertNotEqual(b.modified_ts, c.modified_ts)


# python3 -m unittest -v tests
from unittest import TestCase

from app import app
from models import db, Cupcake
# avoid sorted keys
app.json.sort_keys

URL_PATH = "/api/cupcakes"

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""
        self.client = app.test_client()
        app.config.update({
            "TESTING": True,
            "SQLALCHEMY_ECHO": False,
            "SQLALCHEMY_DATABASE_URI": "postgresql:///cupcake_test",
            "DEBUG_TB_HOSTS": ["dont-show-debug-toolbar"]
        })
                # create an app context
        with app.app_context():
            db.drop_all()
            db.create_all()

            cupcake = Cupcake(**CUPCAKE_DATA)
            db.session.add(cupcake)
            db.session.commit()

            self.cupcake = cupcake
            
            print('\n',cupcake)
            Cupcake.query.delete()


    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.rollback()

    def test_list_cupcakes(self):
        with self.client:
            resp = self.client.get(URL_PATH)

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": float(5),
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        """ Test for creating cupcake """
        with self.client:
            url = f"{URL_PATH}/{self.cupcake.id}"
            resp = self.client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": float(5),
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        """ Test for creating cupcake """
        with self.client:
            resp = self.client.post(URL_PATH, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": float(10),
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        """ Test for updating cupcake """
        DATA = { 
                "flavor": "raspberry",
                "size": "xsm",
                "rating": 3.0,
                "image": "http://raspberry"
                }
                
        with self.client:
            resp = self.client.patch(f"{URL_PATH}/{self.cupcake.id}", json=DATA)
            data = resp.json
            # get data from db which is the updated cupcake
            with app.app_context():
                cupcake = Cupcake.query.get_or_404(self.cupcake.id)
                self.assertEqual(cupcake.serialize_cupcake(), {
                        "flavor": DATA['flavor'],
                        "id": self.cupcake.id,
                        "image": DATA['image'],
                        "rating": DATA['rating'],
                        "size": DATA['size']
                    }
                )

    def test_delete_cupcake(self):
        """ Test for deleting cupcake """
        with self.client:
            with app.app_context():
                resp = self.client.delete(f"{URL_PATH}/{self.cupcake.id}")
                ck = Cupcake.query.get(1)
                self.assertEqual(resp.status_code, 200)
                # no cupcake found will return None
                self.assertEqual(None, ck)
                # hit delete route again this time cupcake_id will not exist
                resp = self.client.delete(f"{URL_PATH}/{self.cupcake.id}")
                # cupcake is not in database and should return 404 status code
                self.assertEqual(resp.status_code, 404)
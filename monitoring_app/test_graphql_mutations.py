from graphene_django.utils.testing import GraphQLTestCase
from .schema import schema

class MetricMutationTests(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema

    def test_create_metric_negative_value(self):
        response = self.query(query='''
            mutation {
                createMetric(name: "Test", value: -5) {
                    metric {
                        id
                        name
                        value
                    }
                }
            }
        ''')
        print("Status Code:", response.status_code)
        print("Content:", response.content.decode())
        content = response.json()
        self.assertIsNone(content.get('data', {}).get('createMetric'))
        self.assertTrue('errors' in content)
        self.assertEqual(content['errors'][0]['message'], "Metric value cannot be negative.")

    def test_create_metric_negative_value(self):
        response = self.query(
        query='''
            mutation {
                createMetric(name: "Test", value: -5) {
                    metric {
                        id
                        name
                        value
                    }
                }
            }
        ''',
       url = "/graphql/"  # <-- important!
    )
        print("Status Code:", response.status_code)
        print("Content:", response.content.decode())
        content = response.json()
        self.assertIsNone(content.get('data', {}).get('createMetric'))
        self.assertTrue('errors' in content)
        self.assertEqual(content['errors'][0]['message'], "Metric value cannot be negative.")

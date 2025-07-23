from flask import Blueprint
from flask_restx import Api, Resource, marshal
from lutils.decorators import requires_fields_validation, requires_json

VERSION = '1.0'
DOC = 'teste-mb API'

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint,
          version=VERSION,
          title='teste-mb API',
          description=DOC,
          doc='/docs/swagger',
          authorizations={
              'x-api-key': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': 'x-api-key'
              },
              'Token': {
                  'type': 'apiKey',
                  'in': 'header',
                  'name': 'Authorization'
              }
          })

ns = api.namespace('', description='teste-mb API endpoints')

@ns.route('/', '/healthz', doc=False)
class Index(Resource):
    def get(self):
        return dict(
            service='teste-mb API HealthCheck',
            version=VERSION)

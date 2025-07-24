import logging
from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource
from json import loads

from main.application_layer.use_cases.address import AddressUseCase
from main.application_layer.use_cases.transaction import TransactionUseCase
from main.application_layer.use_cases.transfer import TransferUseCase
from main.presentation_layer.views.schemas import validate_model, transfer_model
from main.presentation_layer.mappings import ValidateMapping, TransferMapping

logger = logging.getLogger("teste-mb." + __name__)

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

api.models[validate_model.name] = validate_model
api.models[transfer_model.name] = transfer_model

@ns.route('/', '/healthz', doc=False)
class Index(Resource):
    def get(self):
        return dict(
            service='teste-mb API HealthCheck',
            version=VERSION)
    
@ns.route('/generate')
class Generate(Resource):
    def post(self):
        data = request.get_json()
        quantity = data.get('quantity', 1)

        address_usecase = AddressUseCase()
        try:
            return jsonify({'status': 'success', 'generated_addresses': address_usecase.generate(quantity=quantity)}), 201
        except Exception as e:
            logger.exception(
                "Generate requested failed",
                extra={
                    "props": {
                        "request": "/api/generate",
                        "method": "POST",
                        "quantity": 1,
                        "error_message": str(e)
                    }
                })
            return {"message": str(e)}, 400    

@ns.route('/addresses')
class Addresses():
    def get(self):
        try:
            address_usecase = AddressUseCase()

            return jsonify([
                {"uuid": a.uuid, "address": a.address} for a in address_usecase.get()
            ]), 200
        except Exception as e:
            logger.exception(
                "Addresses requested failed",
                extra={
                    "props": {
                        "request": "/api/addresses",
                        "method": "POST",
                        "quantity": 1,
                        "error_message": str(e)
                    }
                })
            return {"message": str(e)}, 400
        
@ns.route('/validate')
class Validate(Resource):

    @ns.expect(validate_model)
    @ns.response(200, 'OK')
    def post(self):

        mapping = ValidateMapping(payload=loads(request.data))
        
        try:

            transaction_usecase = TransactionUseCase()
            return transaction_usecase.validate(tx_hash=mapping.tx_hash)

        except Exception as e:
            logger.exception(
                "Validate requested failed",
                extra={
                    "props": {
                        "request": "/api/validate",
                        "method": "POST",
                        "quantity": 1,
                        "error_message": str(e)
                    }
                })
            return {"message": str(e)}, 400

@ns.route('/transactions')
class Transactions(Resource):

    @ns.expect(validate_model)
    @ns.response(200, 'OK')
    def get(self):

        try:

            transaction_usecase = TransactionUseCase()
            transaction_usecase.get_transanctions()

        except Exception as e:
            logger.exception(
                "Transactions requested failed",
                extra={
                    "props": {
                        "request": "/api/transactions",
                        "method": "GET",
                        "quantity": 1,
                        "error_message": str(e)
                    }
                })
            return {"message": str(e)}, 400
        
@ns.route('/transfer')
class Transfers(Resource):

    @ns.expect(transfer_model)
    @ns.response(200, 'OK')
    def post(self):
        transfer_mapping = TransferMapping(payload=loads(request.data))

        try:

            transfer_usecase = TransferUseCase()
            result = transfer_usecase.execute(
                from_address=transfer_mapping.from_address,
                private_key=transfer_mapping.private_key,
                to_address=transfer_mapping.to_address,
                asset=transfer_mapping.asset,
                amount=transfer_mapping.amount
            )

            return result
        
        except Exception as e:
            logger.exception(
                "Transfer requested failed",
                extra={
                    "props": {
                        "request": "/api/transfer",
                        "method": "POST",
                        "from_address": transfer_mapping.from_address,
                        "private_key": transfer_mapping.private_key,
                        "to_address": transfer_mapping.to_address,
                        "asset": transfer_mapping.asset,
                        "amount": transfer_mapping.amount,
                        "error_message": str(e)
                    }
                })
            return {"message": str(e)}, 400

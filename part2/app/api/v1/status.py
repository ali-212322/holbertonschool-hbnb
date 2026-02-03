from flask_restx import Namespace, Resource

api = Namespace("status", description="API Status")

@api.route("/")
class StatusResource(Resource):
    def get(self):
        return {"status": "OK"}, 200

import falcon
from server.services.candidate import Candidate as Candidateservice


class Candidate:
    def __init__(self):
        self.service = Candidateservice()

    def on_get(self, req, resp):
        pass

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200

        # input_file = req.get_param('file')

        # if input_file.filename:
        #     ext = input_file.filename.split('.')[1]
        #     data = from_stream(input_file.file, ext)
        #     resp.status = falcon.HTTP_200
        #     resp.body = data

# class candidate:
# 	def on_get(self, req, resp):
#            pass
#
# 	def on_get_id(self, req, resp, id):
# 		resp.status = falcon.HTTP_200
# 		resp.body = f'id: {id}'
#
# 	def on_get_name(self, req, resp, name):
# 		resp.status = falcon.HTTP_200
# 		resp.body = f'name: {name}'

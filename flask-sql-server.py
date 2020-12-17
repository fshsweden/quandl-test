import falcon, json

class ClosingPricesResource(object):

  # companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

  def on_get(self, req, resp):

    #
    # get all closing prices for product XYZ and DATE RANGE D1 -> D2
    #
    print(req)
    resp.body = json.dumps(self.companies)

  def on_post(self, req, resp):
    #
    # save closing price for product XYZ and DATE d
    #
    print(req)
    raw_data = json.load(req.bounded_stream)
    print(raw_data)
    resp.status = falcon.HTTP_201
    resp.body = json.dumps({"success": True})

api = falcon.API()
cp_endpoint = ClosingPricesResource()
api.add_route('/closing_prices', cp_endpoint)

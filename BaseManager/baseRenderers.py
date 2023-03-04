from rest_framework import renderers
import json

class BaseJsonRenderer(renderers.JSONRenderer):
  charset="utf-8"
  def render(self, data, accepted_media_type=None, renderer_context=None):
    if "ErrorDetail" in str(data):
      return json.dumps({"errors":data})
    
    return json.dumps(data)
    
   
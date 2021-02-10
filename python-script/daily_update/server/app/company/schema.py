from marshmallow import fields, Schema


class SearchSchema(Schema):
    """Search schema"""

    #doodadId = fields.Number(attribute="doodad_id")
    name = fields.String(attribute="name")
    purpose = fields.String(attribute="purpose")

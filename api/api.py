from flask import Flask, jsonify, request
from flask_restful import Resource, Api, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from marshmallow import Schema, fields

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/src/api/checklists.db'
db = SQLAlchemy(app)


##### MODELS #####


class Checklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('ChecklistItem',
                            backref=db.backref('checklist', lazy='joined'),
                            lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Checklist(name='%s')>" % self.name


class ChecklistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist.id'))
    is_check = db.Column(db.Boolean(False))

    def __init__(self, name, checklist_id):
        self.name = name
        self.checklist_id = checklist_id

    def __repr__(self):
        return "<ChecklistItem(name='%s', checklist_id='%s')>" % \
               (self.name, self.checklist_id)


##### SCHEMAS #####

class ChecklistItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    checklist_id = fields.Int()
    is_check = fields.Boolean()


class ChecklistSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    items = fields.Nested(nested=ChecklistItemSchema(), many=True, only=('name', 'is_check'))


##### API ENDPOINTS #####


class ChecklistsResource(Resource):
    def get(self):
        checklists = Checklist.query.all()
        result = ChecklistSchema(many=True).dump(checklists)
        return jsonify(result.data)

    def post(self):
        checklist = Checklist(request.json.get('name'))
        db.session.add(checklist)
        db.session.commit()

        result = ChecklistSchema().dump(Checklist.query.get(checklist.id))
        return jsonify(result.data)


class ChecklistResource(Resource):
    def get(self, checklist_id):
        try:
            checklist = Checklist.query.get(checklist_id)
            result = ChecklistSchema().dump(checklist)
            return jsonify(result.data)
        except IntegrityError:
            return jsonify({"message": "Checklist not found."}), 404

    def delete(self, checklist_id):
        try:
            checklist = Checklist.query.get(checklist_id)
            db.session.delete(checklist)
            db.session.commit()

            return jsonify({'deleted': True})
        except IntegrityError:
            return jsonify({"message": "Checklist not found."}), 404


class ChecklistItemsResource(Resource):
    def post(self, checklist_id):
        try:
            checklist = Checklist.query.get(checklist_id)

            item = ChecklistItem(request.json.get('name'), checklist.id)
            db.session.add(item)
            db.session.commit()
            result = ChecklistItemSchema().dump(ChecklistItem.query.get(item.id))

            return jsonify(result.data)
        except IntegrityError:
            return jsonify({"message": "Checklist or item not found."}), 404


class ChecklistItemResource(Resource):
    def patch(self, checklist_id, item_id):
        try:
            checklist = Checklist.query.get(checklist_id)
            checklist_item = checklist.items.filter(ChecklistItem.id == item_id).first()
            checklist_item.is_check = request.json.get('is_check')
            db.session.commit()

            result = ChecklistItemSchema().dump(ChecklistItem.query.get(checklist_item.id))

            return jsonify(result.data)
        except IntegrityError:
            return jsonify({"message": "Checklist or item not found."}), 404

    def delete(self, checklist_id, item_id):
        try:
            checklist = Checklist.query.get(checklist_id)
            checklist_item = checklist.items.filter(ChecklistItem.id == item_id)
            checklist_item.delete()
            db.session.commit()

            return jsonify({'deleted': True})
        except IntegrityError:
            return jsonify({"message": "Checklist or item not found."}), 404


api.add_resource(ChecklistsResource, '/api/checklists')
api.add_resource(ChecklistResource, '/api/checklists/<checklist_id>')
api.add_resource(ChecklistItemsResource, '/api/checklists/<checklist_id>/items')
api.add_resource(ChecklistItemResource, '/api/checklists/<checklist_id>/items/<item_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)

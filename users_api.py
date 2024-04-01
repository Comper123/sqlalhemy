from data import db_session
from flask import abort, jsonify, make_response
from data.users import User
from flask_restful import reqparse, abort, Api, Resource


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('position', required=True)
parser.add_argument('speciality', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('city_from', required=True)


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {
                'users': [u.to_dict(only=('surname', 
                                        'name', 
                                        'age',
                                        'position',
                                        'speciality',
                                        'address',
                                        'email',
                                        'city_from')) for u in users]
            }
        )
    
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            city_from=args['city_from']
        )
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('surname', 
                  'name', 
                  'age',
                  'position',
                  'speciality',
                  'address',
                  'email',
                  'city_from'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        if not user:
            return make_response(jsonify({'error': 'Not found'}), 404)
        args = parser.parse_args()
        if 'surname' in args:
            user.surname = args['surname']
        if 'name' in args:
            user.name = args['name']
        if 'age' in args:
            user.age = args['age']
        if 'position' in args:
            user.position = args['position']
        if 'speciality' in args:
            user.speciality = args['speciality']
        if 'address' in args:
            user.address = args['address']
        if 'email' in args:
            user.email = args['email']
        if 'address' in args:
            user.city_from = args['city_from']

        db_sess.commit()
        return jsonify({'success': 'OK'})
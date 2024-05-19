
from flask import Blueprint, request, jsonify, Response

from sqlalchemy import asc, desc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError, DataError, StatementError

from user_api.database.db import db, User

bp = Blueprint('users', __name__, url_prefix='/api/users')


# GET list of all the Users
@bp.route('', methods=['GET'])
def get_all_users():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)
    search = request.args.get('search')

    try:
        sort_param = request.args.get('sort', 'id')
        if sort_param.startswith('-'):
            sort_attr = sort_param[1:]
            
        else:
            sort_attr = sort_param
            
        sort = getattr(User, sort_attr)
    except AttributeError:
        sort = User.id
        
    
    if search is not None:
        users = User.query.filter(
            (User.first_name.ilike(f'%{search}%')) |
            (User.last_name.ilike(f'%{search}%'))
        )
    else:
        users = User.query
    
    users = users.order_by(sort).paginate(page=page, per_page=limit)

    return jsonify([i.to_dict() for i in users]), 200

#GET filters the users with id

@bp.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    try:
        user = User.query.filter(User.id == id).one()
        return jsonify(user.to_dict())
    except NoResultFound:
        return Response(status=404)



# POST data to Users
@bp.route('', methods=['POST'])
def add_user():
    
    data = request.get_json()
    if data is None:
        return Response(status=400)
    
    """required_fields = ['id', 'first_name', 'last_name', 'company_name', 'city', 'state', 'zip', 'email', 'web', 'age']
    if not all(field in data for field in required_fields):
        return Response(status=400) """
    
   
    new_user = User(
        id=data['id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        company_name=data['company_name'],
        city=data['city'],
        state=data['state'],
        zip=data['zip'],
        email=data['email'],
        web=data['web'],
        age=data['age']
    )
    try: 
        db.session.add(new_user)
        db.session.commit()
        return Response(status=201)
    except (IntegrityError, TypeError, DataError, StatementError) as e:
        db.session.rollback()
        return Response(status=400)
    except:
        db.session.rollback()
        return Response(status=500)

#PUT Update the user
@bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()

    if not data:
        return Response(status=400)
    
    try:
        user = User.query.filter(User.id == id).one()
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return Response(status=200)
    except NoResultFound:
        return Response(status=404)
    except (IntegrityError, TypeError, DataError, StatementError) as e:
        db.session.rollback()
        return Response(status=400)
    except:
        db.session.rollback()
        return Response(status=500)
    

#DELETE the user
@bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter(User.id == id).one()
        db.session.delete(user)
        db.session.commit()
        return Response(status=200)
    except NoResultFound:
        return Response(status=404)
    except:
        db.session.rollback()
        return Response(status=500)

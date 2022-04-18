import flask

from . import db_session
from .users import User
from flask import jsonify, redirect

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return redirect('/my_training')
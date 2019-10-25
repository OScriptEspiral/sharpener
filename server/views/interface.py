from flask import Blueprint, session, render_template


def create_interface_blueprint(db_session, debug):
    interface = Blueprint('interface', __name__)

    @interface.route('/', defaults={'path': ''}, methods=['GET'])
    @interface.route('/<path:path>', methods=['GET'])
    def serve_template(path):
        return render_template('index.html',
                               email=session.get('email'),
                               name=session.get('name'),
                               nickname=session.get('nickname'),
                               token=session.get('token'),
                               avatar=session.get('avatar'),
                               is_logged_in='email' in session,
                               debug=debug)
    return interface

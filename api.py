import flask
from data import db_session
from data.jobs import Jobs


blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return flask.jsonify(
        {
            'jobs': [j.to_dict(only=('job', 
                                     'work_size', 
                                     'collaborators',
                                     'is_finished',
                                     'team_leader')) for j in jobs]
        }
    )
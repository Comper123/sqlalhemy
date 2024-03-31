import flask
from data import db_session
from data.jobs import Jobs
from flask import jsonify, make_response, request

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


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_news(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobs_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'job': job.to_dict(only=('job', 
                                     'work_size', 
                                     'collaborators',
                                     'is_finished',
                                     'team_leader'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)
    elif not all(key in flask.request.json for key in
                 ['job', 'work_size', 'collaborators', 'is_finished', 'team_leader']):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    job = Jobs(
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
        team_leader=request.json['team_leader']
    )
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'id': job.id})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_job(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobs_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def update_job(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobs_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    if 'job' in request.json:
        job.job = request.json['job']
    if 'work_size' in request.json:
        job.work_size = request.json['work_size']
    if 'collaborators' in request.json:
        job.collaborators = request.json['collaborators']
    if 'is_finished' in request.json:
        job.is_finished = request.json['is_finished']
    if 'team_leader' in request.json:
        job.team_leader = request.json['team_leader']
    db_sess.commit()
    return jsonify({'success': 'OK'})
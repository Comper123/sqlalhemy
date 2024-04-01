from data import db_session
from flask import abort, jsonify, make_response
from data.jobs import Jobs
from flask_restful import reqparse, abort, Api, Resource


def abort_if_job_not_found(jobs_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(jobs_id)
    if not job:
        abort(404, message=f"Job {jobs_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('job', required=True)
parser.add_argument('collaborators', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('team_leader', required=True, type=int)


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify(
            {
                'jobs': [j.to_dict(only=('job', 
                                        'collaborators', 
                                        'work_size',
                                        'is_finished',
                                        'team_leader')) for j in jobs]
            }
        )
    
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            job=args['job'],
            collaborators=args['collaborators'],
            work_size=args['work_size'],
            is_finished=args['is_finished'],
            team_leader=args['team_leader']
        )
        session.add(job)
        session.commit()
        return jsonify({'id': job.id})


class JobResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('job', 
                  'collaborators', 
                  'work_size',
                  'is_finished',
                  'team_leader'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, job_id):
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).get(job_id)
        if not job:
            return make_response(jsonify({'error': 'Not found'}), 404)
        args = parser.parse_args()
        if 'job' in args:
            job.job = args['job']
        if 'collaborators' in args:
            job.collaborators = args['collaborators']
        if 'work_size' in args:
            job.work_size = args['work_size']
        if 'is_finished' in args:
            job.is_finished = args['is_finished']
        if 'team_leader' in args:
            job.team_leader = args['team_leader']

        db_sess.commit()
        return jsonify({'success': 'OK'})
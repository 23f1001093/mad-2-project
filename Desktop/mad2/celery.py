from celery import Celery

def make_celery(app):
    # Create a new Celery object with Flask app name
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )

    # Configure celery using Flask app's config
    celery.conf.update(app.config)

    # Create task context so tasks run inside Flask app context
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

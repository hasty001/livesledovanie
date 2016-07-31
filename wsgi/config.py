import os

OPENSHIFT_MONGODB_DB_URL = "mongodb://admin:51dBVLs4ZLpi@%s:%s/sledovanie" \
                           %(os.environ['OPENSHIFT_MONGODB_DB_HOST'],os.environ['OPENSHIFT_MONGODB_DB_PORT'])
#creating a shell context 
import sqlalchemy as sa
import sqlalchemy.orm as so
#That initial line changed to this for creating a new shell context for db
from app import app,db
from app.models import User,Post

#The Initial single line was for blogproject
#from app import app,db

@app.shell_context_processor
def make_shell_context():
    return {'sa':sa,'so':so,'db':db,'User':User,'Post':Post}
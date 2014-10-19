import os
import urllib
import cgi

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)





owner=""

class Home(webapp2.RequestHandler):
  def get(self):
    global owner
    user = users.get_current_user()

    if user:
        owner=user.nickname()
        template = JINJA_ENVIRONMENT.get_template('index.html')
        template_values = {
            'name': 'Welcom '+user.nickname()+' ,',

            
        }
        self.response.write(template.render(template_values ))
        

    else:
        self.redirect(users.create_login_url(self.request.uri))


class Logout(webapp2.RequestHandler):
  def get(self):
    self.redirect(users.create_logout_url('/'))





class Portfolio(webapp2.RequestHandler):
  def get(self):
    greets = Photo.query(Photo.owner == owner).fetch()

    url=[]
    for greeting in greets:
      
      
      blob_key = blobstore.get(str(greeting.image))

      img = images.Image(blob_key=blob_key)


      info = {
        "lien":    images.get_serving_url(blob_key),
        "titre": greeting.titre,
        "description":  greeting.description,
        }
    
      url.append(info)
      

    #self.response.out.write(url[0])


    
    template = JINJA_ENVIRONMENT.get_template('portfolio1.html')
    template_values = {
            'url': url,
            
        }
    self.response.write(template.render(template_values ))
    
class Portfolio2(webapp2.RequestHandler):
  def get(self):
    greets = Photo.query(Photo.owner == owner).fetch()

    url=[]
    for greeting in greets:
      
      
      blob_key = blobstore.get(str(greeting.image))

      img = images.Image(blob_key=blob_key)


      info = {
        "lien":    images.get_serving_url(blob_key),
        "titre": greeting.titre,
        "description":  greeting.description,
        }
    
      url.append(info)
      

    #self.response.out.write(url[0])


    
    template = JINJA_ENVIRONMENT.get_template('portfolio.html')
    template_values = {
            'url': url,
            
        }
    self.response.write(template.render(template_values ))
   

   
class Index(webapp2.RequestHandler):
  def get(self):
    

    template = JINJA_ENVIRONMENT.get_template('index.html')
    template_values = {
            'name': '',
            
        }
    self.response.write(template.render(template_values ))

class Contact(webapp2.RequestHandler):
  def get(self):
    

    template = JINJA_ENVIRONMENT.get_template('contact.html')
    template_values = {
            'name': 'slim',
            
        }
    self.response.write(template.render(template_values ))
  


class About(webapp2.RequestHandler):
  def get(self):
    

    template = JINJA_ENVIRONMENT.get_template('about.html')
    template_values = {
            'name': 'slim',
            
        }
    self.response.write(template.render(template_values ))

class Services(webapp2.RequestHandler):
  def get(self):
    

    template = JINJA_ENVIRONMENT.get_template('services.html')
    template_values = {
            'name': 'slim',
            
        }
    self.response.write(template.render(template_values ))

class Upload(webapp2.RequestHandler):
  def get(self):
    
    upload_url = blobstore.create_upload_url('/put')
    template = JINJA_ENVIRONMENT.get_template('upload1.html')
    template_values = {
            'upload_url': upload_url,
            
            
        }
    self.response.write(template.render(template_values ))





class Upload2(webapp2.RequestHandler):

  def get(self):
    
    upload_url = blobstore.create_upload_url('/put')
    template = JINJA_ENVIRONMENT.get_template('upload.html')
    template_values = {
            'upload_url': upload_url,
            
            
        }
    self.response.write(template.render(template_values ))



class Album(webapp2.RequestHandler):
  def get(self):

    greets = Photo.query(Photo.owner == owner).fetch()

    url=[]
    for greeting in greets:
      
      
      blob_key = blobstore.get(str(greeting.image))

      img = images.Image(blob_key=blob_key)


      info = {
        "lien":    images.get_serving_url(blob_key),
        "titre": greeting.titre,
        "description":  greeting.description,
        }
    
      url.append(info)
      

    #self.response.out.write(url[0])


    
    template = JINJA_ENVIRONMENT.get_template('album.html')
    template_values = {
            'url': url,
            
        }
    self.response.write(template.render(template_values ))
    

   

class Trait(webapp2.RequestHandler):
    def get(self):

        image_name = self.request.get('text')
        
        #self.response.out.write(image_name )
        template = JINJA_ENVIRONMENT.get_template('trait.html')
        template_values = {
                'name': image_name,
                
            }
        self.response.write(template.render(template_values ))

class Delete(webapp2.RequestHandler):
  def get(self,id):


    greets = Photo.query(Photo.description == id).fetch()

    greets[0].key.delete()
    
    
    self.redirect('/portfolio2')
class Magic(webapp2.RequestHandler):
  def get(self):
    greets = Photo.query(Photo.owner == owner).fetch()

    url=[]
    for greeting in greets:
      
      
      blob_key = blobstore.get(str(greeting.image))

      img = images.Image(blob_key=blob_key)


      info = {
        "lien":    images.get_serving_url(blob_key),
        "titre": greeting.titre,
        "description":  greeting.description,
        }
    
      url.append(info)
      

    #self.response.out.write(url[0])


    
    template = JINJA_ENVIRONMENT.get_template('magic.html')
    template_values = {
            'url': url,
            
        }
    self.response.write(template.render(template_values ))
    

   


class Test(webapp2.RequestHandler):
  def get(self):
    
    upload_url = blobstore.create_upload_url('/put')
    template = JINJA_ENVIRONMENT.get_template('test.html')
    template_values = {
             'upload_url': upload_url,
            
        }
    self.response.write(template.render(template_values ))

DEFAULT_IMAGE_NAME="test"
def image_key(image_name=DEFAULT_IMAGE_NAME):
    
    return ndb.Key('Guestbook', image_name)


class Photo(ndb.Model):
    
    
    titre = ndb.StringProperty(indexed=False)
    owner = ndb.StringProperty()
    description = ndb.StringProperty()
    image = ndb.BlobKeyProperty()







class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):

    upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
    blob_info = upload_files[0]
    image_name = self.request.get('text',
                               DEFAULT_IMAGE_NAME)
    greeting = Photo(parent=image_key(image_name))


    greeting.titre = self.request.get('text')
    greeting.owner = owner
    greeting.description= self.request.get('text2')
    greeting.image = blob_info.key()

    greeting.put()


    self.redirect('/upload2')


class Effect(webapp2.RequestHandler):
  def get(self):
    greets = Photo.query(Photo.owner == owner).fetch()

    url=[]
    for greeting in greets:
      
      
      blob_key = blobstore.get(str(greeting.image))

      img = images.Image(blob_key=blob_key)


      info = {
        "lien":    images.get_serving_url(blob_key),
        "titre": greeting.titre,
        "description":  greeting.description,
        }
    
      url.append(info)
      

    #self.response.out.write(url[0])


    
    template = JINJA_ENVIRONMENT.get_template('effect.html')
    template_values = {
            'url': url,
            
        }
    self.response.write(template.render(template_values ))

class Trait2(webapp2.RequestHandler):
  def get(self):

    image_name = self.request.get('text')
    
    #self.response.out.write(image_name )
    template = JINJA_ENVIRONMENT.get_template('traiteffect.html')
    template_values = {
            'name': image_name,
            
        }
    self.response.write(template.render(template_values ))



application = webapp2.WSGIApplication([
    
    ('/', Home),
    ('/effect', Effect),
    ('/index',Index),
    ('/logout',Logout),
    ('/portfolio',Portfolio),
    ('/portfolio2',Portfolio2),
    ('/about',About),
    ('/contact',Contact),
    ('/services',Services),
    ('/upload',Upload),
    ('/upload2',Upload2),
    ('/album',Album),
    ('/magic',Magic),
    ('/put', UploadHandler),
    ('/test',Test),
    webapp2.Route('/@<id:.*>', handler=Delete),
    webapp2.Route('/work', handler=Trait),
    webapp2.Route('/effe', handler=Trait2),

    
], debug=True)

 
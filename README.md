# dev-busca
Django app for highlighting some dev and their projects. It is inspired by <a href="https://www.udemy.com/course/python-django-2021-complete-course/">this</a> udemy course

<a href="https://devbusca.herokuapp.com/">Live preview</a>


# highlights:
- signup, login, logout users
- restrict certains actions to only logged in users
- restrict certains actions to only the user who created base action in the 1st place
- create, edit, delete projects, skills related to a particular user
# key learning points:
- how to query & access data of the db directly in templates using "_set"
- django is still stuck in the past and doesn't support login/signup with email by default. One has to go through some extreme gymnastic to get there. How then is it used for production worldwide?
- conditionnaly render templates when the same template is used for 2 or more views
- how to style and add atributes to form's inputs right in the forms.py
- how to use __icontains, __iexact, __in while performing search queries

# todos:
- change login from using username to email
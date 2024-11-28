from django.shortcuts import render,redirect


class AuthMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response
    self.auth_routes = ('/usuario/login/', '/usuario/cadastrar/')

  def __call__(self, request):
    print(request.path)
    if request.user.is_authenticated:
        if request.path in self.auth_routes:
          return redirect('index')
    elif request.path not in self.auth_routes:
        return redirect('usuarios:login')
    return self.get_response(request)
    # print(request.user.is_authenticated, request.path)

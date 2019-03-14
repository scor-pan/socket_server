# simple_app.py


def simple_app(environ, start_response):
	'''
	simple_app()函数就是一个符合WSGI标准的HTTP处理函数，它接受两个参数：
		environ :一个包含所有HTTP请求信息的 dict 对象
		start_response :一个发送HTTP响应的函数
	'''
	status = '200 OK'
	response_headers = [('Content-type', 'text/plain')]
	start_response(status, response_headers)
	'''
	在simple_app()函数中，调用：start_response('200 OK',[('Content-Type','text/plain')]
	就发送了HTTP响应的Header，注意Header只能发送一次，也就是只能调用一次start_response函数。
	
	start_response()函数接受两个参数：
		一个是HTTP响应码
		一个是一组list 表示的HTTP Header，每个Header用一个包含两str 的tuple 表示。
	'''
	return [b'Hello world! -by the5ire \n']
	
	'''然后，函数的返回值[b'Hello world! -by the5ire \n'] 讲作为HTTP响应的body 发送给浏览器'''
	'''这个simple_app()函数本身没有涉及到任何解析HTTP的部分，也就是底层代码不需要编写，我们只负责在更高层次上考虑如何响应请求就可以了'''
		
	
	


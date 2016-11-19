#coding=utf-8

def log(func):
    def wrapper(*args, **kw):
        print('===call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

def logWithParam(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s ===call %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

def logWithParamOrNot(text = 'test'):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s ===call %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

def logWithPrint(func):
    def wrapper(*args, **kw):
        print('begin call %s():' % func.__name__)
        func(*args, **kw)
        print('end call %s():' % func.__name__)
    return wrapper

@logWithPrint
def now():
    print('2016-05-17')
    
if __name__ == '__main__':
    now()
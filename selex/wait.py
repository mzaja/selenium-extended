def wait(time: float): 
    """
    Intended for use as a decorator within the Driver class. 
    Forces the implicit wait on executing the class methods.
    Example:
        @wait(5)
        def method(self, *args, **kwargs)
        ->
        method is executed with an implicit webdriver wait of 5 seconds.
    """
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            old_wait = self.implicit_wait
            self.implicit_wait = time
            try:
                return method(self, *args, **kwargs)
            finally:
                self.implicit_wait = old_wait
        return wrapper
    return decorator


def wait_factory(driver_attr_name: str):
    """
    Returns a wait decorator for a webdriver class atribute named driver_attr_name.
    Example:
        wait = wait_factory("driver")
        
        class HasDriverAsAttribute:
            def __init__(self):
                self.driver = Driver("Chrome")
            
            @wait(5)
            def method(self, *args, **kwargs):
                <Does something with self.driver>
        
        -> method is executed with an implicit webdriver wait of 5 seconds
    """
    def wait(time: float): 
        """
        Intended for use as a decorator within the Driver class. 
        Forces the implicit wait on executing the class methods.
        Example:
            @wait(5)
            def method(self, *args, **kwargs)
            ->
            method is executed with an implicit webdriver wait of 5 seconds.
        """
        def decorator(method):
            def wrapper(self, *args, **kwargs):
                old_wait = getattr(self, driver_attr_name).implicit_wait
                getattr(self, driver_attr_name).implicit_wait = time
                try:
                    return method(self, *args, **kwargs)
                finally:
                    getattr(self, driver_attr_name).implicit_wait = old_wait
            return wrapper
        return decorator
    return wait
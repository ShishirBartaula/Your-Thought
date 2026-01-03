class ExampleMiddleware:

    def __init__(self,get_response)->None:
        # This runs only once when the server starts.
        # It remembers who is "next in line" (the view or the next middleware).
        self.get_response=get_response

    def __call__(self,request, *args, **kwargs):
         # This runs for EVERY single request a user makes.
         
        print("MiddleWare called")
         # 2. PASS THE BALL
        # This line sends the request to the actual View (like tweet_list)
        # and waits for the answer (the HTML page).
        response=self.get_response(request)
        
        # 3. POST-PROCESSING (After the View)
        # The view has finished, and we have the response

        user_agent=request.META.get('HTTP_USER_AGENT')

        print("########")
        print(user_agent)
        print("#######")

        return response
    
from django.core.cache import cache

class OnlineNowMiddleware(object):
    
    def process_request(self, request):

        #Getting the IP address of the user
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[0]
        else:
            user_ip = request.META.get('REMOTE_ADDR')

        # Getting the list of current online users
        online = cache.get('online_now')

        if online:
            online = [ip for ip in online if cache.get(ip)]
        else:
            online = []

        # Adding the new IP to the cache, assuming that the user will be online for 10 mins
        cache.set(user_ip, True, 600) 

        # Adding the new IP to the list
        if user_ip not in online:
            online.append(user_ip)

        cache.set('online_now', online)

        # List of online users and count added to request
        request.__class__.online_now = online
        request.__class__.online_now_count = len(online)

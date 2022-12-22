from fake_useragent import UserAgent


class GetUserAgent:
    
    def random_user_agent(self):
        ua = UserAgent()
        user_agent_dict = { 'User-Agent': ua.random }
        return user_agent_dict
    
# if __name__ == "__main__":
#     user_agent_instance = GetUserAgent()
#     random_user_agent = user_agent_instance.random_user_agent()
    
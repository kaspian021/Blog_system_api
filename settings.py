import os


class Settings:
    def __init__(self):
        self.DATABASE_URL = 'sqlite: // /./ sql_app.db'
        self.SECRET_KEY = 'uJ0 - IUZNGdjD5j6hBkm7CQEu9 - hPU - fiw94U8DT_jjw'
        self.ALGORITHM = 'HS256'
        self.TOKEN_TIME_AUTHENTICATION = 1440
        self.GOGGLE_CLIENT_ID =''
        self.GOGGLE_CLIENT_SECRET =''
        self.SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4dGVzYXV2a2F0dGt3aHF1eG9zIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1OTQ3OTk5MiwiZXhwIjoyMDc1MDU1OTkyfQ.TgXWnIsdezOE_d2hRQDD1ZmEJWy1IucKQrY3Re4zVjI'
        self.SUPABASE_URL = 'https: // rxtesauvkattkwhquxos.supabase.co'
        # استفاده از os.environ به جای os.getenv
        # self.DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///./sql_app.db')
        # self.SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-change-me')
        # self.ALGORITHM = os.environ.get('ALGORITHM', 'HS256')
        # self.GOGGLE_CLIENT_ID = os.environ.get('GOGGLE_CLIENT_ID', '')
        # self.GOGGLE_CLIENT_SECRET = os.environ.get('GOGGLE_CLIENT_SECRET', '')
        # self.SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'default-supabase-key')
        # self.SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://default.supabase.co')
        # self.TOKEN_TIME_AUTHENTICATION = int(os.environ.get('TOKEN_TIME_AUTHENTICATION', '30'))

        print("Environment variables:")
        print("DATABASE_URL:", self.DATABASE_URL)
        print("SUPABASE_KEY:", self.SUPABASE_KEY)
        print("SUPABASE_URL:", self.SUPABASE_URL)
        print("SECRET_KEY:", self.SECRET_KEY)


settings = Settings()
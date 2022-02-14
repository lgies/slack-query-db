CREATE ROLE anon nologin;
GRANT USAGE ON SCHEMA public TO anon;

GRANT SELECT ON public.user_profile TO anon;
GRANT SELECT ON public.country TO anon;

CREATE ROLE authenticator noinherit login PASSWORD 'password';
GRANT anon TO authenticator;

CREATE ROLE slackbot nologin;
GRANT slackbot TO authenticator;
GRANT USAGE ON SCHEMA public TO slackbot;

GRANT ALL ON public.user_profile TO slackbot;
GRANT ALL ON public.country TO slackbot;

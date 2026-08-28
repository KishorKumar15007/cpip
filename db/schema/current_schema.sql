-- Auto-generated snapshot for reference only. Source of truth is alembic/versions/. Regenerate with: pg_dump --schema-only ...
--
-- PostgreSQL database dump
--

\ restrict kHdWRTkI9LRiGCw33aEb4RmzZ0pg7o5FurCPVaclbvBp9yOcm8Dwo9rIy0PH7Je -- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;
SET default_tablespace = '';
SET default_table_access_method = heap;
--
-- Name: ContestParticipation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ContestParticipation" (
    participation_id bigint NOT NULL,
    user_id bigint NOT NULL,
    platform text NOT NULL,
    contest_id text NOT NULL,
    contest_name text NOT NULL,
    rank integer,
    old_rating integer,
    new_rating integer,
    participated_at timestamp with time zone NOT NULL
);
--
-- Name: ContestParticipation_participation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public."ContestParticipation"
ALTER COLUMN participation_id
ADD GENERATED ALWAYS AS IDENTITY (
        SEQUENCE NAME public."ContestParticipation_participation_id_seq" START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
    );
--
-- Name: OAuthIdentities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."OAuthIdentities" (
    identity_id bigint NOT NULL,
    user_id bigint NOT NULL,
    provider text NOT NULL,
    provider_id text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_oauthidentities_provider CHECK (
        (
            provider = ANY (ARRAY ['google'::text, 'github'::text])
        )
    )
);
--
-- Name: OAuthIdentities_identity_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public."OAuthIdentities"
ALTER COLUMN identity_id
ADD GENERATED ALWAYS AS IDENTITY (
        SEQUENCE NAME public."OAuthIdentities_identity_id_seq" START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
    );
--
-- Name: PasswordCredentials; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."PasswordCredentials" (
    user_id bigint NOT NULL,
    password_hash text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);
--
-- Name: ProblemTags; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ProblemTags" (
    problem_id bigint NOT NULL,
    tag_id bigint NOT NULL
);
--
-- Name: Problems; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Problems" (
    problem_id bigint NOT NULL,
    platform text NOT NULL,
    platform_problem_id text NOT NULL,
    title text NOT NULL,
    platform_difficulty text,
    cf_rating integer,
    url text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT "Problems_cf_rating_check" CHECK (
        (
            (cf_rating IS NULL)
            OR (cf_rating > 0)
        )
    ),
    CONSTRAINT "Problems_platform_check" CHECK (
        (
            platform = ANY (ARRAY ['codeforces'::text, 'leetcode'::text])
        )
    )
);
--
-- Name: Problems_problem_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public."Problems"
ALTER COLUMN problem_id
ADD GENERATED ALWAYS AS IDENTITY (
        SEQUENCE NAME public."Problems_problem_id_seq" START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
    );
--
-- Name: RefreshTokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."RefreshTokens" (
    refresh_token_id bigint NOT NULL,
    user_id bigint NOT NULL,
    token_hash text NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    revoked_at timestamp with time zone
);
--
-- Name: RefreshTokens_refresh_token_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public."RefreshTokens"
ALTER COLUMN refresh_token_id
ADD GENERATED ALWAYS AS IDENTITY (
        SEQUENCE NAME public."RefreshTokens_refresh_token_id_seq" START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
    );
--
-- Name: Submissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Submissions" (
    submission_id bigint NOT NULL,
    user_id bigint NOT NULL,
    session_id bigint,
    problem_id bigint NOT NULL,
    platform text NOT NULL,
    platform_submission_id text NOT NULL,
    verdict text NOT NULL,
    language text NOT NULL,
    submitted_at timestamp with time zone NOT NULL,
    attempt_number integer NOT NULL,
    CONSTRAINT "Submissions_attempt_number_check" CHECK ((attempt_number > 0))
);
--
-- Name: Submissions_submission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public."Submissions"
ALTER COLUMN submission_id
ADD GENERATED ALWAYS AS IDENTITY (
        SEQUENCE NAME public."Submissions_submission_id_seq" START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
    );
--
-- Name: Tags; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Tags" (
    tag_id bigint NOT NULL,
    name text NOT NULL
);
--
-- Name: Tags_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public."Tags"
ALTER COLUMN tag_id
ADD GENERATED ALWAYS AS IDENTITY (
        SEQUENCE NAME public."Tags_tag_id_seq" START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
    );
--
-- Name: User; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."User" (
    user_id bigint NOT NULL,
    username text NOT NULL,
    email text,
    lc_username text,
    cf_username text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    cf_last_synced_at timestamp with time zone,
    lc_last_synced_at timestamp with time zone
);
--
-- Name: UserSessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."UserSessions" (
    session_id bigint NOT NULL,
    user_id bigint NOT NULL,
    started_at timestamp with time zone NOT NULL,
    ended_at timestamp with time zone NOT NULL,
    CONSTRAINT "UserSessions_check" CHECK ((ended_at > started_at))
);
--
-- Name: UserSessions_session_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public."UserSessions"
ALTER COLUMN session_id
ADD GENERATED ALWAYS AS IDENTITY (
        SEQUENCE NAME public."UserSessions_session_id_seq" START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
    );
--
-- Name: User_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public."User"
ALTER COLUMN user_id
ADD GENERATED ALWAYS AS IDENTITY (
        SEQUENCE NAME public."User_user_id_seq" START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1
    );
--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (version_num character varying(32) NOT NULL);
--
-- Name: ContestParticipation ContestParticipation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ContestParticipation"
ADD CONSTRAINT "ContestParticipation_pkey" PRIMARY KEY (participation_id);
--
-- Name: OAuthIdentities OAuthIdentities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."OAuthIdentities"
ADD CONSTRAINT "OAuthIdentities_pkey" PRIMARY KEY (identity_id);
--
-- Name: PasswordCredentials PasswordCredentials_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."PasswordCredentials"
ADD CONSTRAINT "PasswordCredentials_pkey" PRIMARY KEY (user_id);
--
-- Name: ProblemTags ProblemTags_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProblemTags"
ADD CONSTRAINT "ProblemTags_pkey" PRIMARY KEY (problem_id, tag_id);
--
-- Name: Problems Problems_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Problems"
ADD CONSTRAINT "Problems_pkey" PRIMARY KEY (problem_id);
--
-- Name: RefreshTokens RefreshTokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RefreshTokens"
ADD CONSTRAINT "RefreshTokens_pkey" PRIMARY KEY (refresh_token_id);
--
-- Name: Submissions Submissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Submissions"
ADD CONSTRAINT "Submissions_pkey" PRIMARY KEY (submission_id);
--
-- Name: Tags Tags_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Tags"
ADD CONSTRAINT "Tags_name_key" UNIQUE (name);
--
-- Name: Tags Tags_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Tags"
ADD CONSTRAINT "Tags_pkey" PRIMARY KEY (tag_id);
--
-- Name: UserSessions UserSessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserSessions"
ADD CONSTRAINT "UserSessions_pkey" PRIMARY KEY (session_id);
--
-- Name: User User_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."User"
ADD CONSTRAINT "User_email_key" UNIQUE (email);
--
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."User"
ADD CONSTRAINT "User_pkey" PRIMARY KEY (user_id);
--
-- Name: User User_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."User"
ADD CONSTRAINT "User_username_key" UNIQUE (username);
--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);
--
-- Name: ContestParticipation uq_contestparticipation_user_id_platform_contest_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ContestParticipation"
ADD CONSTRAINT uq_contestparticipation_user_id_platform_contest_id UNIQUE (user_id, platform, contest_id);
--
-- Name: OAuthIdentities uq_oauthidentities_provider_provider_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."OAuthIdentities"
ADD CONSTRAINT uq_oauthidentities_provider_provider_id UNIQUE (provider, provider_id);
--
-- Name: OAuthIdentities uq_oauthidentities_user_provider; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."OAuthIdentities"
ADD CONSTRAINT uq_oauthidentities_user_provider UNIQUE (user_id, provider);
--
-- Name: Problems uq_problems_platform_platform_problem_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Problems"
ADD CONSTRAINT uq_problems_platform_platform_problem_id UNIQUE (platform, platform_problem_id);
--
-- Name: RefreshTokens uq_refreshtokens_token_hash; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RefreshTokens"
ADD CONSTRAINT uq_refreshtokens_token_hash UNIQUE (token_hash);
--
-- Name: Submissions uq_submission_platform_platform_submission_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Submissions"
ADD CONSTRAINT uq_submission_platform_platform_submission_id UNIQUE (platform, platform_submission_id);
--
-- Name: idx_contestparticipation_user_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_contestparticipation_user_date ON public."ContestParticipation" USING btree (user_id, participated_at);
--
-- Name: idx_contestparticipation_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_contestparticipation_user_id ON public."ContestParticipation" USING btree (user_id);
--
-- Name: idx_problems_platform; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_problems_platform ON public."Problems" USING btree (platform);
--
-- Name: idx_problemtags_problem_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_problemtags_problem_id ON public."ProblemTags" USING btree (problem_id);
--
-- Name: idx_problemtags_tag_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_problemtags_tag_id ON public."ProblemTags" USING btree (tag_id);
--
-- Name: idx_submissions_problem_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_submissions_problem_id ON public."Submissions" USING btree (problem_id);
--
-- Name: idx_submissions_session_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_submissions_session_id ON public."Submissions" USING btree (session_id);
--
-- Name: idx_submissions_submitted_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_submissions_submitted_at ON public."Submissions" USING btree (submitted_at);
--
-- Name: idx_submissions_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_submissions_user_id ON public."Submissions" USING btree (user_id);
--
-- Name: idx_submissions_user_problem; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_submissions_user_problem ON public."Submissions" USING btree (user_id, problem_id);
--
-- Name: idx_usersessions_user_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_usersessions_user_id ON public."UserSessions" USING btree (user_id);
--
-- Name: ContestParticipation ContestParticipation_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ContestParticipation"
ADD CONSTRAINT "ContestParticipation_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id);
--
-- Name: OAuthIdentities OAuthIdentities_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."OAuthIdentities"
ADD CONSTRAINT "OAuthIdentities_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id) ON DELETE CASCADE;
--
-- Name: PasswordCredentials PasswordCredentials_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."PasswordCredentials"
ADD CONSTRAINT "PasswordCredentials_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id) ON DELETE CASCADE;
--
-- Name: ProblemTags ProblemTags_problem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProblemTags"
ADD CONSTRAINT "ProblemTags_problem_id_fkey" FOREIGN KEY (problem_id) REFERENCES public."Problems"(problem_id);
--
-- Name: ProblemTags ProblemTags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProblemTags"
ADD CONSTRAINT "ProblemTags_tag_id_fkey" FOREIGN KEY (tag_id) REFERENCES public."Tags"(tag_id);
--
-- Name: RefreshTokens RefreshTokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RefreshTokens"
ADD CONSTRAINT "RefreshTokens_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id) ON DELETE CASCADE;
--
-- Name: Submissions Submissions_problem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Submissions"
ADD CONSTRAINT "Submissions_problem_id_fkey" FOREIGN KEY (problem_id) REFERENCES public."Problems"(problem_id);
--
-- Name: Submissions Submissions_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Submissions"
ADD CONSTRAINT "Submissions_session_id_fkey" FOREIGN KEY (session_id) REFERENCES public."UserSessions"(session_id);
--
-- Name: Submissions Submissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Submissions"
ADD CONSTRAINT "Submissions_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id);
--
-- Name: UserSessions UserSessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserSessions"
ADD CONSTRAINT "UserSessions_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(user_id);
--
-- PostgreSQL database dump complete
--

\ unrestrict kHdWRTkI9LRiGCw33aEb4RmzZ0pg7o5FurCPVaclbvBp9yOcm8Dwo9rIy0PH7Je

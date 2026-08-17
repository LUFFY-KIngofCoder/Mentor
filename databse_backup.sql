--
-- PostgreSQL database dump
--

\restrict gde2GOtNMWuhxcFkpZRJUa0rh43yUHpuNHnkbHMog1FmZNyZFzOncpK4MKzLzE8

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: commitments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.commitments (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    title character varying NOT NULL,
    description character varying,
    duration_days integer NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    status character varying NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);


ALTER TABLE public.commitments OWNER TO postgres;

--
-- Name: daily_entries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.daily_entries (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    date date NOT NULL,
    sleep_hours double precision,
    deep_work_hours double precision,
    distraction_hours double precision,
    mood_score integer,
    energy_score integer,
    journal_entry character varying,
    what_avoided character varying,
    biggest_win character varying,
    biggest_failure character varying,
    what_can_be_different character varying,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);


ALTER TABLE public.daily_entries OWNER TO postgres;

--
-- Name: metric_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.metric_logs (
    id uuid NOT NULL,
    daily_entry_id uuid NOT NULL,
    metric_id uuid NOT NULL,
    value double precision NOT NULL,
    created_at timestamp with time zone,
    is_successful boolean DEFAULT false NOT NULL
);


ALTER TABLE public.metric_logs OWNER TO postgres;

--
-- Name: missed_day_reflections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.missed_day_reflections (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    missed_date date NOT NULL,
    reason character varying NOT NULL,
    reflection character varying NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);


ALTER TABLE public.missed_day_reflections OWNER TO postgres;

--
-- Name: tracking_metrics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tracking_metrics (
    id uuid NOT NULL,
    commitment_id uuid NOT NULL,
    name character varying NOT NULL,
    metric_type character varying NOT NULL,
    operator character varying NOT NULL,
    target_value double precision NOT NULL
);


ALTER TABLE public.tracking_metrics OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid NOT NULL,
    email character varying NOT NULL,
    password_hash character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone DEFAULT now(),
    name character varying NOT NULL,
    day_reset_hour integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
43fe7e041818
\.


--
-- Data for Name: commitments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.commitments (id, user_id, title, description, duration_days, start_date, end_date, status, created_at, updated_at) FROM stdin;
4a9dc3fa-efbd-481d-874e-e69de65c0436	157965a9-72a8-4baa-b68a-98246a02f731	Study	study atelast 2 hours a day	30	2026-06-23	2026-07-23	active	2026-05-23 19:53:12.59451+05:30	2026-06-24 16:28:31.989292+05:30
78be0e20-cf97-4932-8649-a29ce005fd2d	2c525321-4fa3-496a-ad08-ba536df6e595	Level 2	Make 1 hour of Deep work , Workout and the whoel routine my identity	30	2026-08-11	2026-09-10	active	2026-08-11 10:52:53.018343+05:30	2026-08-11 10:52:53.018343+05:30
\.


--
-- Data for Name: daily_entries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.daily_entries (id, user_id, date, sleep_hours, deep_work_hours, distraction_hours, mood_score, energy_score, journal_entry, what_avoided, biggest_win, biggest_failure, what_can_be_different, created_at, updated_at) FROM stdin;
79356c4a-8188-435c-9beb-2bd44b396e65	157965a9-72a8-4baa-b68a-98246a02f731	2026-06-21	0	0	0	0	0						2026-06-21 20:02:52.455531+05:30	2026-06-21 20:02:52.455531+05:30
97168b75-e2c9-4c60-9ef9-8ea0b884014e	157965a9-72a8-4baa-b68a-98246a02f731	2026-06-20	11	1	9	\N	8	idk	\N	\N	\N	\N	2026-06-21 20:16:57.960796+05:30	2026-06-21 20:16:57.960796+05:30
0d14935d-076e-48d8-b8db-83cb3bda1313	2c525321-4fa3-496a-ad08-ba536df6e595	2026-08-11	\N	\N	\N	\N	\N	\N	\N	\N	\N	\N	2026-08-11 10:53:09.060783+05:30	2026-08-11 10:53:09.060783+05:30
76b58351-543c-4361-8774-a3767889404e	157965a9-72a8-4baa-b68a-98246a02f731	2026-08-11	2	0	0	0	0	string	string	string	string	string	2026-08-12 00:04:11.485115+05:30	2026-08-12 01:20:07.450915+05:30
\.


--
-- Data for Name: metric_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.metric_logs (id, daily_entry_id, metric_id, value, created_at, is_successful) FROM stdin;
45cd4161-01dd-4875-ac01-e0087718cefe	79356c4a-8188-435c-9beb-2bd44b396e65	02ccf80b-24df-471d-995f-3f3c117d6adf	2	2026-06-21 20:07:12.4161+05:30	f
50ff5015-9954-4431-b1c4-ee35df65819a	97168b75-e2c9-4c60-9ef9-8ea0b884014e	02ccf80b-24df-471d-995f-3f3c117d6adf	2	2026-06-21 20:16:57.97091+05:30	f
581663a1-e046-44b4-a603-51268d5c3990	0d14935d-076e-48d8-b8db-83cb3bda1313	f883d508-55af-437d-89ab-0a38456a88d9	1	2026-08-11 10:53:09.084382+05:30	t
ee1fd02f-da45-43cc-b374-f960e5c2cd40	0d14935d-076e-48d8-b8db-83cb3bda1313	37a4b8d7-29b7-4d5c-ad46-52ab27b08e6d	1	2026-08-11 10:53:17.004381+05:30	t
4c063e9f-9053-42ea-b27c-58deaf43252a	0d14935d-076e-48d8-b8db-83cb3bda1313	9ed0cb16-e91c-42d2-9d91-f600bd61a480	1	2026-08-11 10:53:21.207186+05:30	t
c1de1233-d263-49d0-b681-657ee392b120	0d14935d-076e-48d8-b8db-83cb3bda1313	a92db68c-7cf4-483c-b2dd-43d2617434de	1	2026-08-11 10:53:27.401645+05:30	t
\.


--
-- Data for Name: missed_day_reflections; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.missed_day_reflections (id, user_id, missed_date, reason, reflection, created_at, updated_at) FROM stdin;
e2ffd045-b69b-4e96-9dc5-650faaf2ff5a	157965a9-72a8-4baa-b68a-98246a02f731	2026-05-23	meri galti thi 	ki maine aur mehnat nhi ki lekin aur zyada karunga\n	2026-06-24 16:26:12.436269+05:30	2026-06-24 16:26:12.436269+05:30
cbe5d1ee-d540-42b2-9310-2d20064806a3	157965a9-72a8-4baa-b68a-98246a02f731	2026-06-23	thak gaya tha 	mehnat aur krani padegi\n	2026-06-24 16:29:10.272811+05:30	2026-06-24 16:29:10.272811+05:30
9b5b6227-0b91-4cc8-a192-d9fa601c3695	157965a9-72a8-4baa-b68a-98246a02f731	2026-06-24	 	 	2026-08-11 13:44:00.0228+05:30	2026-08-11 13:44:00.0228+05:30
aea97ad9-4f73-4156-9288-a31db8c2494b	157965a9-72a8-4baa-b68a-98246a02f731	2026-06-25	 	 	2026-08-11 13:44:01.67182+05:30	2026-08-11 13:44:01.67182+05:30
d72b403a-0a97-40bd-887d-dc36c965e7e7	157965a9-72a8-4baa-b68a-98246a02f731	2026-06-26	 	  	2026-08-11 13:44:04.104884+05:30	2026-08-11 13:44:04.104884+05:30
6743ede5-8542-48ee-9cb8-b08d2c36c151	157965a9-72a8-4baa-b68a-98246a02f731	2026-06-27	 	 	2026-08-11 13:44:05.895706+05:30	2026-08-11 13:44:05.895706+05:30
6f314af7-6c8f-4563-99fe-e20cf98d7763	157965a9-72a8-4baa-b68a-98246a02f731	2026-06-28	 	 	2026-08-11 13:44:07.211215+05:30	2026-08-11 13:44:07.211215+05:30
51a671fc-2531-4e27-b2d1-285073eee508	157965a9-72a8-4baa-b68a-98246a02f731	2026-06-29	 	 	2026-08-11 13:44:08.977857+05:30	2026-08-11 13:44:08.977857+05:30
f99131fc-7ccf-4751-9c44-304a98ddb25c	157965a9-72a8-4baa-b68a-98246a02f731	2026-06-30	 	 	2026-08-11 13:44:10.286994+05:30	2026-08-11 13:44:10.286994+05:30
7a3b9936-e2db-43d3-8c55-3d4ac456604d	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-01	 	 	2026-08-11 13:44:11.972696+05:30	2026-08-11 13:44:11.972696+05:30
dcf925f3-7bb7-483a-b6c4-2fbe9af230b6	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-02	 	 	2026-08-11 13:44:14.04984+05:30	2026-08-11 13:44:14.04984+05:30
27f85956-abbd-4300-a82e-071fd1dcd9b8	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-03	 	 	2026-08-11 13:44:15.323384+05:30	2026-08-11 13:44:15.323384+05:30
8d4f515f-2ad1-48fb-8b8e-e7d4283240de	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-04	 	 	2026-08-11 13:44:16.638615+05:30	2026-08-11 13:44:16.638615+05:30
b4b48baa-e017-49c0-9264-62f8a1945696	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-05	 	 	2026-08-11 13:44:18.034945+05:30	2026-08-11 13:44:18.034945+05:30
1dbe655b-6a17-4558-9227-4df650de9e50	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-06	 	 	2026-08-11 13:44:19.415347+05:30	2026-08-11 13:44:19.415347+05:30
72995668-d3b9-40e8-8fb7-24d9fa6f1c39	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-07	 	 	2026-08-11 13:44:21.809519+05:30	2026-08-11 13:44:21.809519+05:30
21e78d35-a99c-4868-96b8-de330e768a92	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-08	 	 	2026-08-11 13:44:24.777149+05:30	2026-08-11 13:44:24.777149+05:30
848cfd41-f51d-4cd9-8272-f26e980e7e50	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-09	 	 	2026-08-11 13:44:26.634104+05:30	2026-08-11 13:44:26.634104+05:30
9cce44f0-f7bf-40b3-b15d-1d6bd4df8f9e	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-10	 	 	2026-08-11 13:44:28.307027+05:30	2026-08-11 13:44:28.307027+05:30
2cd9e9a6-0432-4d27-9240-5ee76370108e	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-11	 	 	2026-08-11 13:44:29.904702+05:30	2026-08-11 13:44:29.904702+05:30
a477e41a-9f90-42f1-b530-26c8ce33fc37	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-12	 	 	2026-08-11 13:44:31.530521+05:30	2026-08-11 13:44:31.530521+05:30
90ff3316-01ea-4d2b-b8b1-cecc73996d1a	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-13	 	 	2026-08-11 13:44:33.568424+05:30	2026-08-11 13:44:33.568424+05:30
e90b1fab-a640-4d22-8194-3c0c1fc08e2f	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-14	 	 	2026-08-11 13:44:34.952262+05:30	2026-08-11 13:44:34.952262+05:30
1b089677-b013-4c53-a88e-a3679fdd3a0b	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-15	 	 	2026-08-11 13:44:36.801084+05:30	2026-08-11 13:44:36.801084+05:30
cec03211-985c-42c9-9fb0-6840a84d9ed9	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-16	 	 	2026-08-11 13:44:38.445713+05:30	2026-08-11 13:44:38.445713+05:30
2fdaefae-4775-4b82-a75d-65f82053a69f	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-17	 	 	2026-08-11 13:44:40.341416+05:30	2026-08-11 13:44:40.341416+05:30
95dbd57f-972b-43d9-bb8c-32ec2af3d300	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-18	 	 	2026-08-11 13:44:42.171772+05:30	2026-08-11 13:44:42.171772+05:30
7ed80ad1-aac9-4be5-85d7-d404953f77e5	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-19	 	 	2026-08-11 13:44:43.625401+05:30	2026-08-11 13:44:43.625401+05:30
0515606b-8383-48f0-857a-cbe750aa50f4	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-20	 	 	2026-08-11 13:44:45.026902+05:30	2026-08-11 13:44:45.026902+05:30
bb95bfbe-37b9-4d15-8ac4-082dffc7ad41	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-21	 	 	2026-08-11 13:44:47.905424+05:30	2026-08-11 13:44:47.906423+05:30
29d2a0a0-abad-4020-9574-500d77f81032	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-22	 	 \n	2026-08-11 13:44:52.804653+05:30	2026-08-11 13:44:52.804653+05:30
9e847559-15da-46e5-821e-3723b3d1efff	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-23	 	 	2026-08-11 13:44:54.712675+05:30	2026-08-11 13:44:54.712675+05:30
5a03856b-22e4-46e1-ac2b-11aef46f6705	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-24	 	 	2026-08-11 13:44:56.591497+05:30	2026-08-11 13:44:56.591497+05:30
1bbac0ea-a766-4076-851b-3dafdde9ac60	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-25	 	 	2026-08-11 13:44:58.137083+05:30	2026-08-11 13:44:58.137083+05:30
9f1b9efa-3635-40a7-8b4d-cb5176d6269e	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-26	 	 	2026-08-11 13:44:59.652531+05:30	2026-08-11 13:44:59.652531+05:30
b170d828-4092-4909-80d6-b19fb3235618	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-27	 	 	2026-08-11 13:45:01.323471+05:30	2026-08-11 13:45:01.323471+05:30
0c0cc0bb-6a80-445d-9a24-4c7922b9e2d9	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-28	 	 	2026-08-11 13:45:02.982519+05:30	2026-08-11 13:45:02.982519+05:30
ba818dcd-e3b9-4715-86b9-67f40fcc3a3b	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-29	 	 	2026-08-11 13:45:05.380523+05:30	2026-08-11 13:45:05.380523+05:30
2f92f18c-6772-4d66-afab-abadacfdf71d	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-30	 	 	2026-08-11 13:45:07.52485+05:30	2026-08-11 13:45:07.52485+05:30
c335e610-b787-4d7e-b90b-889f243a9f67	157965a9-72a8-4baa-b68a-98246a02f731	2026-07-31	 	 	2026-08-11 13:45:09.174133+05:30	2026-08-11 13:45:09.174133+05:30
1595af5a-60bb-41be-8ec3-5f62fbf1c130	157965a9-72a8-4baa-b68a-98246a02f731	2026-08-01	 	 	2026-08-11 13:45:11.275055+05:30	2026-08-11 13:45:11.275055+05:30
017f77af-db2c-4640-a1a6-20995e75f3eb	157965a9-72a8-4baa-b68a-98246a02f731	2026-08-02	 	 	2026-08-11 13:45:12.743155+05:30	2026-08-11 13:45:12.743155+05:30
1fc35efc-f9cb-4e2f-8dbf-4cc8c7666dfd	157965a9-72a8-4baa-b68a-98246a02f731	2026-08-03	 	 	2026-08-11 13:45:14.639123+05:30	2026-08-11 13:45:14.639123+05:30
ce0af416-f592-4b28-b874-454379b5210c	157965a9-72a8-4baa-b68a-98246a02f731	2026-08-04	 	 	2026-08-11 13:45:16.119158+05:30	2026-08-11 13:45:16.119158+05:30
7effcbf5-0c69-4c88-bcb4-dd6b4a9a9b81	157965a9-72a8-4baa-b68a-98246a02f731	2026-08-05	 	 	2026-08-11 13:45:17.701176+05:30	2026-08-11 13:45:17.701176+05:30
70bcb357-1692-4288-9d5a-fecc2bf7538d	157965a9-72a8-4baa-b68a-98246a02f731	2026-08-06	 	 	2026-08-11 13:45:19.108926+05:30	2026-08-11 13:45:19.108926+05:30
d8697865-f6e9-4e3a-ad74-42b7fd41831d	157965a9-72a8-4baa-b68a-98246a02f731	2026-08-07	 	 	2026-08-11 13:45:20.56772+05:30	2026-08-11 13:45:20.56772+05:30
002d4bf4-b0bd-4e98-89c0-9ff77fbad9b4	157965a9-72a8-4baa-b68a-98246a02f731	2026-08-08	 	 	2026-08-11 13:45:21.956028+05:30	2026-08-11 13:45:21.956028+05:30
2f2e496e-14ed-438c-b479-f605ea738201	157965a9-72a8-4baa-b68a-98246a02f731	2026-08-09	 	 	2026-08-11 13:45:23.698131+05:30	2026-08-11 13:45:23.698131+05:30
cc77c751-45ae-49a2-a8dd-76c9bbbff494	157965a9-72a8-4baa-b68a-98246a02f731	2026-08-10	idk	idk	2026-08-11 21:52:07.795549+05:30	2026-08-11 21:52:07.795549+05:30
\.


--
-- Data for Name: tracking_metrics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tracking_metrics (id, commitment_id, name, metric_type, operator, target_value) FROM stdin;
02ccf80b-24df-471d-995f-3f3c117d6adf	4a9dc3fa-efbd-481d-874e-e69de65c0436	study hour	hours	>=	2
9ed0cb16-e91c-42d2-9d91-f600bd61a480	78be0e20-cf97-4932-8649-a29ce005fd2d	Wake up at 6:00 a.m.	boolean	>=	1
37a4b8d7-29b7-4d5c-ad46-52ab27b08e6d	78be0e20-cf97-4932-8649-a29ce005fd2d	Sleep at 11:00pm	boolean	>=	1
f883d508-55af-437d-89ab-0a38456a88d9	78be0e20-cf97-4932-8649-a29ce005fd2d	Workout	boolean	>=	1
a92db68c-7cf4-483c-b2dd-43d2617434de	78be0e20-cf97-4932-8649-a29ce005fd2d	1 Hour Deep Work	hours	>=	1
5f074efc-b334-4e0d-9c0b-e0753477ebf0	4a9dc3fa-efbd-481d-874e-e69de65c0436	sleep	hour	>=	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, password_hash, created_at, updated_at, name, day_reset_hour) FROM stdin;
157965a9-72a8-4baa-b68a-98246a02f731	sneha@gmail.com	$2b$12$FZ5O048wNWgRFcZS67wJHuxnHJF.2KHFnItUc8beNGwsmsY8hWDuC	2026-05-23 18:42:31.39552+05:30	2026-05-23 18:42:31.39552+05:30	Sneha	0
2c525321-4fa3-496a-ad08-ba536df6e595	shashankghs999@gmail.com	$2b$12$exzs7spoGN.DqKeoARXGreDE.Vmfrj4oL1Pl1RzHNMsUacicdryny	2026-08-11 10:44:30.422309+05:30	2026-08-11 10:44:30.422309+05:30	Shashank	0
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: commitments commitments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commitments
    ADD CONSTRAINT commitments_pkey PRIMARY KEY (id);


--
-- Name: daily_entries daily_entries_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.daily_entries
    ADD CONSTRAINT daily_entries_pkey PRIMARY KEY (id);


--
-- Name: metric_logs metric_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metric_logs
    ADD CONSTRAINT metric_logs_pkey PRIMARY KEY (id);


--
-- Name: missed_day_reflections missed_day_reflections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.missed_day_reflections
    ADD CONSTRAINT missed_day_reflections_pkey PRIMARY KEY (id);


--
-- Name: tracking_metrics tracking_metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tracking_metrics
    ADD CONSTRAINT tracking_metrics_pkey PRIMARY KEY (id);


--
-- Name: daily_entries uq_user_daily_entry; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.daily_entries
    ADD CONSTRAINT uq_user_daily_entry UNIQUE (user_id, date);


--
-- Name: missed_day_reflections uq_user_missed_date; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.missed_day_reflections
    ADD CONSTRAINT uq_user_missed_date UNIQUE (user_id, missed_date);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: commitments commitments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.commitments
    ADD CONSTRAINT commitments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: daily_entries daily_entries_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.daily_entries
    ADD CONSTRAINT daily_entries_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: metric_logs metric_logs_daily_entry_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metric_logs
    ADD CONSTRAINT metric_logs_daily_entry_id_fkey FOREIGN KEY (daily_entry_id) REFERENCES public.daily_entries(id) ON DELETE CASCADE;


--
-- Name: metric_logs metric_logs_metric_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metric_logs
    ADD CONSTRAINT metric_logs_metric_id_fkey FOREIGN KEY (metric_id) REFERENCES public.tracking_metrics(id) ON DELETE CASCADE;


--
-- Name: missed_day_reflections missed_day_reflections_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.missed_day_reflections
    ADD CONSTRAINT missed_day_reflections_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: tracking_metrics tracking_metrics_commitment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tracking_metrics
    ADD CONSTRAINT tracking_metrics_commitment_id_fkey FOREIGN KEY (commitment_id) REFERENCES public.commitments(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict gde2GOtNMWuhxcFkpZRJUa0rh43yUHpuNHnkbHMog1FmZNyZFzOncpK4MKzLzE8


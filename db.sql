PGDMP                      |           vacit    16.3    16.3                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            	           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            
           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16398    vacit    DATABASE     �   CREATE DATABASE vacit WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE vacit;
                postgres    false                       0    0    DATABASE vacit    ACL     %   GRANT ALL ON DATABASE vacit TO root;
                   postgres    false    4875            �            1259    16421    candidate_jobs    TABLE     �   CREATE TABLE public.candidate_jobs (
    id integer NOT NULL,
    job_id integer NOT NULL,
    candidate_id integer NOT NULL,
    motivation text DEFAULT 'Geen motivatie ingevoerd.'::text,
    is_invited boolean DEFAULT false NOT NULL
);
 "   DROP TABLE public.candidate_jobs;
       public         heap    postgres    false            �            1259    16459    candidate_jobs_id_seq    SEQUENCE     �   ALTER TABLE public.candidate_jobs ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.candidate_jobs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    217            �            1259    16407    jobs    TABLE     O  CREATE TABLE public.jobs (
    id integer NOT NULL,
    post_date date DEFAULT CURRENT_DATE NOT NULL,
    company_id integer NOT NULL,
    level character varying(100) NOT NULL,
    title character varying(100) NOT NULL,
    location character varying(100) NOT NULL,
    description text NOT NULL,
    technique_id integer NOT NULL
);
    DROP TABLE public.jobs;
       public         heap    postgres    false            �            1259    16460    jobs_id_seq    SEQUENCE     �   ALTER TABLE public.jobs ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.jobs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    216            �            1259    16429 
   techniques    TABLE     �   CREATE TABLE public.techniques (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    logo_img character varying(255) NOT NULL
);
    DROP TABLE public.techniques;
       public         heap    postgres    false            �            1259    16461    techniques_id_seq    SEQUENCE     �   ALTER TABLE public.techniques ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.techniques_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    218            �            1259    16400    users    TABLE     �  CREATE TABLE public.users (
    id integer NOT NULL,
    role character varying(20) NOT NULL,
    email character varying(100) NOT NULL,
    pswd text NOT NULL,
    name character varying(100) NOT NULL,
    last_name character varying(100),
    address character varying(200),
    postal_code character varying(10),
    city character varying(50),
    profile_img text DEFAULT 'static/img/default.jpg'::text NOT NULL,
    resume_pdf text,
    date_of_birth date,
    mobile character varying(20)
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    16462    users_id_seq    SEQUENCE     �   ALTER TABLE public.users ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    215                       0    16421    candidate_jobs 
   TABLE DATA           Z   COPY public.candidate_jobs (id, job_id, candidate_id, motivation, is_invited) FROM stdin;
    public          postgres    false    217   u"       �          0    16407    jobs 
   TABLE DATA           l   COPY public.jobs (id, post_date, company_id, level, title, location, description, technique_id) FROM stdin;
    public          postgres    false    216   �"                 0    16429 
   techniques 
   TABLE DATA           8   COPY public.techniques (id, name, logo_img) FROM stdin;
    public          postgres    false    218   X%       �          0    16400    users 
   TABLE DATA           �   COPY public.users (id, role, email, pswd, name, last_name, address, postal_code, city, profile_img, resume_pdf, date_of_birth, mobile) FROM stdin;
    public          postgres    false    215   �%                  0    0    candidate_jobs_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.candidate_jobs_id_seq', 5, true);
          public          postgres    false    219                       0    0    jobs_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.jobs_id_seq', 10, true);
          public          postgres    false    220                       0    0    techniques_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.techniques_id_seq', 6, true);
          public          postgres    false    221                       0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 11, true);
          public          postgres    false    222            h           2606    16428 "   candidate_jobs candidate_jobs_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.candidate_jobs
    ADD CONSTRAINT candidate_jobs_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.candidate_jobs DROP CONSTRAINT candidate_jobs_pkey;
       public            postgres    false    217            f           2606    16414    jobs jobs_pkey 
   CONSTRAINT     L   ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id);
 8   ALTER TABLE ONLY public.jobs DROP CONSTRAINT jobs_pkey;
       public            postgres    false    216            j           2606    16433    techniques techniques_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.techniques
    ADD CONSTRAINT techniques_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.techniques DROP CONSTRAINT techniques_pkey;
       public            postgres    false    218            d           2606    16406    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    215            m           2606    16444    candidate_jobs fk_candidate    FK CONSTRAINT     �   ALTER TABLE ONLY public.candidate_jobs
    ADD CONSTRAINT fk_candidate FOREIGN KEY (candidate_id) REFERENCES public.users(id) ON DELETE CASCADE NOT VALID;
 E   ALTER TABLE ONLY public.candidate_jobs DROP CONSTRAINT fk_candidate;
       public          postgres    false    217    215    4708            k           2606    16449    jobs fk_company    FK CONSTRAINT     �   ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT fk_company FOREIGN KEY (company_id) REFERENCES public.users(id) ON DELETE SET NULL NOT VALID;
 9   ALTER TABLE ONLY public.jobs DROP CONSTRAINT fk_company;
       public          postgres    false    215    216    4708            n           2606    16439    candidate_jobs fk_job    FK CONSTRAINT     �   ALTER TABLE ONLY public.candidate_jobs
    ADD CONSTRAINT fk_job FOREIGN KEY (job_id) REFERENCES public.jobs(id) ON DELETE CASCADE NOT VALID;
 ?   ALTER TABLE ONLY public.candidate_jobs DROP CONSTRAINT fk_job;
       public          postgres    false    4710    217    216            l           2606    16454    jobs fk_technique    FK CONSTRAINT     �   ALTER TABLE ONLY public.jobs
    ADD CONSTRAINT fk_technique FOREIGN KEY (technique_id) REFERENCES public.techniques(id) ON DELETE SET NULL NOT VALID;
 ;   ALTER TABLE ONLY public.jobs DROP CONSTRAINT fk_technique;
       public          postgres    false    216    4714    218                (   x�3�4�?�4.cNK�Ȱ�0M9 �%\1z\\\ ֠b      �   �  x���M��@���)�5I���6hFAbf5��a�vW��զ�����G@cn�I��$3�X�k�]��{��X�g���dqQ����C�4��}Eȉb*�7���P�v��l�m�C��jI<��%���-������x)����[tNέa�-�>��S�U�W� �o[ �F>w�K�=���/EJ�	`;$K\�F�Z�!����
a�M�$�|}�u�cBg�P��泃�'��b>/n�,�}�t^��e ,1���������F��1�̎��e"f�1�����QT��;�V>t���aGkV*Uw?��FG]���Ȝ��`���f
�R~ߛ�:���tR��n	M�Ȥ/Rɳ���j�;_�͟=�-�-�Ez+V�1�4AD�����Jab6�"��5tvi+C�r���K98b)&��Q�,E��V$9�bí�c	�^�d*�S�dxRO�؎>+�Q�� &�q�1v�V��F�t�|�KB��Ѻ'��rr}��KZk�����-mT|��j.)f��U�����3b�N|VCrz��AO� a�~���d+0(��!FC$�D8�e5��J/�����;�+ق��Wդ?�YM���7������!l�j�lz������`q@.O��|�����-"�1�����%�}��F��[�E         e   x�3�OMRpI-K��/�M�+����M�/OM�MA���s�r�$�$*'g��%�Bԥ Et�!"`Ef��y)���Ps ݂�Ē���\ݜ��|��=... �+      �   6  x���mk�0�__?�_������*����P�±\�5MJ��K��&�����/��Ǉ�n��|�|YΏ!���(i�a�Ϩ@��#� ���ΥFQFQ^�8�d"A1ֲr��t���{OWD�Y�l�6�QV^���#d��Μ\�`��f��d�)X�u���m���p.�2��b�5/�=��?�0�A����Û���{-��E��*ʊH��V���܅pE5TLM)Qf(ќM}`.�Q�M��*���ln�ܰy��6[�����E��}�}0�ٝ_��u`��Uض>X�1�3���t6E�eYߦ ��     
--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-09-24 19:17:45

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
-- TOC entry 217 (class 1259 OID 41230)
-- Name: categoria; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categoria (
    id_cat integer NOT NULL,
    nombre character varying(50) NOT NULL
);


ALTER TABLE public.categoria OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 41233)
-- Name: categoria_id_cat_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categoria_id_cat_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categoria_id_cat_seq OWNER TO postgres;

--
-- TOC entry 4917 (class 0 OID 0)
-- Dependencies: 218
-- Name: categoria_id_cat_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categoria_id_cat_seq OWNED BY public.categoria.id_cat;


--
-- TOC entry 219 (class 1259 OID 41234)
-- Name: cliente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cliente (
    id_cli integer NOT NULL,
    cli_nombre character varying(100) NOT NULL,
    cli_documento character varying(20) NOT NULL,
    cli_estado boolean DEFAULT true,
    cli_telefono character varying(50),
    cli_direccion character varying(255),
    cli_correo character varying(150)
);


ALTER TABLE public.cliente OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 41238)
-- Name: cliente_id_cli_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cliente_id_cli_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cliente_id_cli_seq OWNER TO postgres;

--
-- TOC entry 4918 (class 0 OID 0)
-- Dependencies: 220
-- Name: cliente_id_cli_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cliente_id_cli_seq OWNED BY public.cliente.id_cli;


--
-- TOC entry 221 (class 1259 OID 41239)
-- Name: detalle_venta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.detalle_venta (
    id_dv integer NOT NULL,
    fk_id_ven integer NOT NULL,
    fk_id_prod integer NOT NULL,
    dv_precio_uni integer NOT NULL,
    dv_total integer NOT NULL,
    dv_cantidad integer NOT NULL,
    dv_estado boolean
);


ALTER TABLE public.detalle_venta OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 41242)
-- Name: detalle_venta_id_dv_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.detalle_venta ALTER COLUMN id_dv ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.detalle_venta_id_dv_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 223 (class 1259 OID 41243)
-- Name: producto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.producto (
    id_prod integer NOT NULL,
    prod_nombre character varying(100) NOT NULL,
    prod_descripcion text,
    prod_precio numeric(10,2) NOT NULL,
    prod_stock integer NOT NULL,
    prod_estado character varying(20) DEFAULT 'Activo'::character varying,
    cantidad integer DEFAULT 0,
    prod_categoria integer
);


ALTER TABLE public.producto OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 41250)
-- Name: producto_id_prod_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.producto ALTER COLUMN id_prod ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.producto_id_prod_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 225 (class 1259 OID 41251)
-- Name: reembolso; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reembolso (
    id_rem integer NOT NULL,
    fk_id_ven integer NOT NULL,
    rem_fecha date NOT NULL,
    rem_valor integer NOT NULL,
    rem_motivo character varying(30) NOT NULL,
    rem_estado boolean
);


ALTER TABLE public.reembolso OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 41254)
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id_usu integer NOT NULL,
    usu_nombre text NOT NULL,
    usu_clave text NOT NULL,
    usu_genero character varying(20) NOT NULL,
    usu_correo character varying(100) NOT NULL,
    usu_estado boolean,
    usu_rol character varying(20) DEFAULT 'empleado'::character varying NOT NULL
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 41260)
-- Name: usuario_id_usu_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.usuario ALTER COLUMN id_usu ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.usuario_id_usu_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 228 (class 1259 OID 41261)
-- Name: venta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.venta (
    id_ven integer NOT NULL,
    ven_fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ven_condicion character varying(10) NOT NULL,
    ven_pago character varying(10) NOT NULL,
    ven_total integer NOT NULL,
    ven_estado boolean DEFAULT true,
    fk_id_cli integer
);


ALTER TABLE public.venta OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 41266)
-- Name: venta_id_ven_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.venta ALTER COLUMN id_ven ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.venta_id_ven_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 4724 (class 2604 OID 41267)
-- Name: categoria id_cat; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categoria ALTER COLUMN id_cat SET DEFAULT nextval('public.categoria_id_cat_seq'::regclass);


--
-- TOC entry 4725 (class 2604 OID 41268)
-- Name: cliente id_cli; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente ALTER COLUMN id_cli SET DEFAULT nextval('public.cliente_id_cli_seq'::regclass);


--
-- TOC entry 4899 (class 0 OID 41230)
-- Dependencies: 217
-- Data for Name: categoria; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categoria (id_cat, nombre) FROM stdin;
1	Confiteria
2	Dulces
3	Galletas
4	Reposteria
5	Snacks
6	Bebidas
\.


--
-- TOC entry 4901 (class 0 OID 41234)
-- Dependencies: 219
-- Data for Name: cliente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cliente (id_cli, cli_nombre, cli_documento, cli_estado, cli_telefono, cli_direccion, cli_correo) FROM stdin;
2	alvaro	4214214	t	\N	\N	\N
3	avas	2142142	t	\N	\N	\N
4	ema	1231312	t	\N	\N	\N
5	MEJIA	10434465	t	3206112513	calle 30a #17-7	\N
6	Maria llinas	108283384	t	3216935764	carrea 34a #29-142	alvarotorresxd5@gmail.com
7	emmanuel	1043447665	t	3206112513	carrea 34a #29-142	mejiaemmanuelandradeinsecaldas@gmail.com
8	Maria llinas	1082833384	t	3216935764	carrea 34a #29-142	llinasmaria8@gmail.com
9	Isabel	1048070671	t	3242692539	Calle 117 # 22b -25 conjunto turpial torre 5 apto 602	oisa2451@gmail.com
10	Jose Luis el parcero 	1032393803	t	316 2314788	santa marta	Joseluisruizmolina@hotmail.com
1	alvaro	1082898253	t	3148657994	carrea 34a #29-142	alvaromanjarrez0906@gmail.com
\.


--
-- TOC entry 4903 (class 0 OID 41239)
-- Dependencies: 221
-- Data for Name: detalle_venta; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.detalle_venta (id_dv, fk_id_ven, fk_id_prod, dv_precio_uni, dv_total, dv_cantidad, dv_estado) FROM stdin;
37	37	30	2000	14000	7	t
38	38	28	500	6000	12	t
39	39	31	20	140	7	t
42	42	31	20	200	10	t
43	43	32	2500	10000	4	t
44	44	30	2000	2000	1	t
45	45	30	2000	2000	1	t
46	46	29	1200	1200	1	t
48	48	31	20	20	1	t
49	49	53	2000	8000	4	t
50	50	53	2000	8000	4	t
51	51	46	2000	12000	6	t
52	52	47	3500	7000	2	t
53	53	49	2500	22500	9	t
54	54	50	2000	6000	3	t
55	55	51	1500	4500	3	t
56	56	52	3000	6000	2	t
57	57	54	2500	15000	6	t
58	58	55	4000	4000	1	t
59	59	56	3500	10500	3	t
60	60	57	5000	10000	2	t
61	61	58	2500	10000	4	t
62	62	59	3000	3000	1	t
63	63	61	300	300	1	t
64	64	60	3500	10500	3	t
65	69	57	5000	10000	2	t
66	69	61	300	600	2	t
67	70	52	3000	6000	2	t
68	70	58	2500	5000	2	t
69	71	47	3500	3500	1	t
70	71	59	3000	3000	1	t
71	71	64	12	12	1	t
72	71	50	2000	2000	1	t
73	71	46	2000	2000	1	t
74	71	53	2000	2000	1	t
75	72	64	12	12	1	t
76	74	54	2500	2500	1	t
77	74	50	2000	2000	1	t
78	74	50	2000	2000	1	t
79	74	62	2500	2500	1	t
80	75	51	1500	4500	3	t
81	76	55	4000	8000	2	t
82	77	51	1500	3000	2	t
83	78	60	3500	14000	4	t
84	79	56	3500	7000	2	t
85	80	49	2500	2500	1	t
86	81	49	2500	2500	1	t
87	82	57	5000	5000	1	t
88	83	61	300	300	1	t
89	84	47	3500	3500	1	t
90	85	59	3000	12000	4	t
91	86	46	2000	2000	1	t
92	87	46	2000	2000	1	t
93	88	46	2000	2000	1	t
94	89	46	2000	6000	3	t
95	90	46	2000	6000	3	t
96	91	53	2000	4000	2	t
97	92	61	300	600	2	t
98	93	47	3500	10500	3	t
99	94	51	1500	7500	5	t
100	95	61	300	600	2	t
101	96	59	3000	6000	2	t
102	97	51	1500	1500	1	t
103	98	51	1500	1500	1	t
104	99	51	1500	1500	1	t
105	100	51	1500	1500	1	t
106	101	51	1500	1500	1	t
107	102	51	1500	1500	1	t
108	103	51	1500	1500	1	t
109	104	46	2000	6000	3	t
110	104	50	2000	6000	3	t
111	104	55	4000	4000	1	t
112	105	46	2000	2000	1	t
113	106	46	2000	2000	1	t
114	107	46	2000	2000	1	t
115	108	46	2000	2000	1	t
116	109	46	2000	2000	1	t
117	110	46	2000	2000	1	t
118	111	46	2000	2000	1	t
119	112	46	2000	2000	1	t
120	113	46	2000	2000	1	t
121	114	46	2000	2000	1	t
122	115	64	12	12	1	t
123	116	52	3000	3000	1	t
124	117	52	3000	3000	1	t
125	118	52	3000	3000	1	t
126	119	58	2500	2500	1	t
127	120	54	2500	2500	1	t
128	121	62	2500	5000	2	t
129	122	64	12	12	1	t
\.


--
-- TOC entry 4905 (class 0 OID 41243)
-- Dependencies: 223
-- Data for Name: producto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.producto (id_prod, prod_nombre, prod_descripcion, prod_precio, prod_stock, prod_estado, cantidad, prod_categoria) FROM stdin;
63	Jugo natural mango 300ml	Bebida refrescante de fruta	4000.00	25	Inactivo	0	6
60	 Maní salado	Bolsa de maní tostado 	3500.00	36	Activo	0	5
56	Muffin vainilla	 Muffin esponjoso con glaseado	3500.00	23	Activo	0	4
49	Bombón chocolate relleno	Bombón con centro de fresa	2500.00	28	Activo	0	2
57	Tarta de queso mini	Porción pequeña de cheesecake	5000.00	14	Activo	0	4
53	 Galleta de chispas	Galleta grande con chispas de chocolate	2000.00	48	Activo	0	3
47	 Caramelo ácido mix	Bolsa surtida de caramelos ácidos	3500.00	36	Activo	0	1
61	 Gaseosa cola 350ml 	Botella individua	300.00	30	Activo	0	6
59	 Maíz inflado dulce	Bolsa de crispetas dulces	3000.00	29	Activo	0	5
51	Nube de azúcar	Malvavisco esponjoso	1500.00	20	Activo	0	2
50	 Tableta de leche 	Chocolate de leche 40g 	2000.00	42	Activo	0	2
55	Brownie chocolate	Brownie húmedo de 80g	4000.00	17	Activo	0	4
46	Chicle menta	Chicle sabor menta, paquete x10	2000.00	28	Activo	0	1
52	Galleta vainilla rellena	Paquete x6 galletas con crema de vainilla	3000.00	22	Activo	0	3
58	Papas fritas clásicas 	Bolsa 50g 	2500.00	59	Activo	0	5
54	Cracker salada	Paquete de galletas saladas	2500.00	40	Activo	0	3
62	Agua mineral 600ml 	Botella sin gas	2500.00	80	Activo	0	6
64	galletas	dulce	12.00	10	Activo	0	3
\.


--
-- TOC entry 4907 (class 0 OID 41251)
-- Dependencies: 225
-- Data for Name: reembolso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reembolso (id_rem, fk_id_ven, rem_fecha, rem_valor, rem_motivo, rem_estado) FROM stdin;
\.


--
-- TOC entry 4908 (class 0 OID 41254)
-- Dependencies: 226
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (id_usu, usu_nombre, usu_clave, usu_genero, usu_correo, usu_estado, usu_rol) FROM stdin;
28	alvaro	scrypt:32768:8:1$honQTfMqnnT10C6e$2c9fccc4bc27b7503cc444e6fa3f130d0c4b21b3f89a717df5104b138eeb1821a838d73efd4219b51d8ece2bfdc12776533ac04dfac09f8a9c5c98a60000f823	masculino	manjarrez@gmail.com	t	dueño
29	mejia	scrypt:32768:8:1$ST07EckKKE6GjMe1$df44d14acd2dcc8f814679ca425869e13e710e95d23b0b130bc358fb43d567fa7c67216b7acc3767667eefae1722ef7a85a5c9c171fcf66f1600710092b96b0e	masculino	mejia2008@gmail.com	t	empleado
\.


--
-- TOC entry 4910 (class 0 OID 41261)
-- Dependencies: 228
-- Data for Name: venta; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.venta (id_ven, ven_fecha, ven_condicion, ven_pago, ven_total, ven_estado, fk_id_cli) FROM stdin;
44	2025-09-13 00:00:00	contado	efectivo	2000	f	1
51	2025-09-14 14:33:49.253619	contado	efectivo	12000	f	1
55	2025-09-14 16:05:38.901282	contado	efectivo	4500	f	1
54	2025-09-14 15:55:02.817627	contado	efectivo	6000	f	1
37	2025-09-12 00:00:00	contado	efectivo	14000	f	1
57	2025-09-15 13:39:05.197841	contado	efectivo	15000	f	1
58	2025-09-15 13:56:34.514532	contado	efectivo	4000	f	1
63	2025-09-15 14:16:23.020297	contado	efectivo	300	f	1
64	2025-09-15 14:20:11.977155	contado	efectivo	10500	f	1
62	2025-09-15 14:16:02.621343	contado	efectivo	3000	f	1
61	2025-09-15 14:15:31.620489	contado	efectivo	10000	f	5
60	2025-09-15 14:15:09.232117	contado	efectivo	10000	f	5
59	2025-09-15 14:08:40.949857	contado	efectivo	10500	f	1
56	2025-09-14 16:29:27.886275	contado	efectivo	6000	f	1
53	2025-09-14 15:53:40.707798	contado	efectivo	22500	f	1
52	2025-09-14 15:32:23.647352	contado	efectivo	7000	f	1
50	2025-09-14 14:33:06.999108	contado	efectivo	8000	f	1
49	2025-09-14 14:32:50.827727	contado	efectivo	8000	f	1
48	2025-09-13 18:51:45.310783	contado	efectivo	20	f	1
46	2025-09-13 00:00:00	contado	efectivo	1200	f	1
45	2025-09-13 00:00:00	contado	efectivo	2000	f	1
43	2025-09-12 00:00:00	contado	efectivo	10000	f	1
42	2025-09-12 00:00:00	contado	efectivo	200	f	1
39	2025-09-12 00:00:00	contado	efectivo	140	f	1
38	2025-09-12 00:00:00	contado	efectivo	6000	f	1
65	2025-09-15 00:00:00	Contado	Efectivo	0	f	1
66	2025-09-15 00:00:00	Contado	Efectivo	0	f	1
69	2025-09-15 15:38:50.625053	contado	efectivo	10600	f	1
68	2025-09-15 00:00:00	Contado	Efectivo	0	f	1
67	2025-09-15 00:00:00	Contado	Efectivo	0	f	1
71	2025-09-15 15:40:32.46879	contado	efectivo	12512	f	1
72	2025-09-15 15:47:22.865505	contado	efectivo	12	f	1
70	2025-09-15 15:39:44.866375	contado	efectivo	11000	f	1
74	2025-09-18 11:39:56.395918	contado	efectivo	9000	f	1
75	2025-09-18 13:17:15.934555	contado	efectivo	4500	t	1
76	2025-09-18 13:38:01.594906	contado	efectivo	8000	t	1
73	2025-09-15 16:31:35.615608	contado	efectivo	0	f	1
77	2025-09-22 14:38:11.534655	contado	efectivo	3000	f	1
78	2025-09-22 14:40:18.141777	contado	efectivo	14000	t	1
79	2025-09-22 15:23:06.971723	contado	efectivo	7000	t	1
80	2025-09-22 21:08:52.339526	contado	efectivo	2500	t	1
81	2025-09-22 21:10:53.305201	contado	efectivo	2500	t	1
82	2025-09-22 21:11:33.398309	contado	efectivo	5000	t	1
83	2025-09-22 21:14:07.503989	contado	efectivo	300	t	1
84	2025-09-22 21:35:43.52286	contado	efectivo	3500	t	1
85	2025-09-22 21:39:57.80809	contado	efectivo	12000	t	6
86	2025-09-22 21:50:30.493201	contado	efectivo	2000	t	1
87	2025-09-22 21:53:12.677857	contado	efectivo	2000	t	1
88	2025-09-22 21:54:11.318947	contado	efectivo	2000	t	1
89	2025-09-22 21:54:40.74327	contado	efectivo	6000	t	1
90	2025-09-22 21:55:09.922635	contado	efectivo	6000	t	1
91	2025-09-22 21:57:47.429466	contado	efectivo	4000	t	1
92	2025-09-22 22:01:21.687269	contado	efectivo	600	t	7
93	2025-09-22 22:02:33.643294	contado	efectivo	10500	t	7
94	2025-09-22 22:05:14.086792	contado	efectivo	7500	t	8
95	2025-09-22 22:11:50.013703	contado	efectivo	600	t	9
96	2025-09-22 22:18:35.529604	contado	efectivo	6000	t	9
97	2025-09-22 22:25:26.422079	contado	efectivo	1500	t	9
98	2025-09-22 22:26:29.985862	contado	efectivo	1500	t	9
99	2025-09-22 22:28:28.803763	contado	efectivo	1500	t	9
100	2025-09-22 22:28:58.551617	contado	efectivo	1500	t	9
101	2025-09-22 22:32:35.035097	contado	efectivo	1500	t	9
102	2025-09-22 22:32:52.164717	contado	efectivo	1500	t	9
103	2025-09-22 22:35:00.191904	contado	efectivo	1500	t	9
104	2025-09-24 17:52:08.483973	contado	efectivo	16000	t	10
105	2025-09-24 18:00:57.002164	contado	efectivo	2000	t	1
106	2025-09-24 18:02:58.969863	contado	efectivo	2000	t	1
107	2025-09-24 18:03:35.530968	contado	efectivo	2000	t	1
108	2025-09-24 18:05:31.322879	contado	efectivo	2000	t	1
109	2025-09-24 18:07:18.580561	contado	efectivo	2000	t	1
110	2025-09-24 18:08:25.632754	contado	efectivo	2000	t	1
111	2025-09-24 18:08:37.428092	contado	efectivo	2000	t	1
112	2025-09-24 18:09:36.556748	contado	efectivo	2000	t	1
113	2025-09-24 18:10:52.099835	contado	efectivo	2000	t	1
114	2025-09-24 18:13:53.834491	contado	efectivo	2000	t	1
115	2025-09-24 18:20:07.751938	contado	efectivo	12	t	1
116	2025-09-24 18:28:13.320865	contado	efectivo	3000	t	1
117	2025-09-24 18:30:48.941251	contado	efectivo	3000	t	1
118	2025-09-24 18:34:03.042911	contado	efectivo	3000	t	1
119	2025-09-24 18:40:28.298983	contado	efectivo	2500	t	1
121	2025-09-24 19:01:25.502195	contado	efectivo	5000	t	1
120	2025-09-24 18:42:38.774015	contado	efectivo	2500	f	1
122	2025-09-24 19:11:19.659818	contado	efectivo	12	t	1
\.


--
-- TOC entry 4919 (class 0 OID 0)
-- Dependencies: 218
-- Name: categoria_id_cat_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categoria_id_cat_seq', 7, true);


--
-- TOC entry 4920 (class 0 OID 0)
-- Dependencies: 220
-- Name: cliente_id_cli_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cliente_id_cli_seq', 10, true);


--
-- TOC entry 4921 (class 0 OID 0)
-- Dependencies: 222
-- Name: detalle_venta_id_dv_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.detalle_venta_id_dv_seq', 129, true);


--
-- TOC entry 4922 (class 0 OID 0)
-- Dependencies: 224
-- Name: producto_id_prod_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.producto_id_prod_seq', 64, true);


--
-- TOC entry 4923 (class 0 OID 0)
-- Dependencies: 227
-- Name: usuario_id_usu_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_id_usu_seq', 29, true);


--
-- TOC entry 4924 (class 0 OID 0)
-- Dependencies: 229
-- Name: venta_id_ven_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.venta_id_ven_seq', 122, true);


--
-- TOC entry 4733 (class 2606 OID 41270)
-- Name: categoria categoria_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categoria
    ADD CONSTRAINT categoria_nombre_key UNIQUE (nombre);


--
-- TOC entry 4735 (class 2606 OID 41272)
-- Name: categoria categoria_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categoria
    ADD CONSTRAINT categoria_pkey PRIMARY KEY (id_cat);


--
-- TOC entry 4737 (class 2606 OID 41274)
-- Name: cliente cliente_cli_documento_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_cli_documento_key UNIQUE (cli_documento);


--
-- TOC entry 4739 (class 2606 OID 41276)
-- Name: cliente cliente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id_cli);


--
-- TOC entry 4741 (class 2606 OID 41278)
-- Name: detalle_venta detalle_venta_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_venta
    ADD CONSTRAINT detalle_venta_pkey PRIMARY KEY (id_dv);


--
-- TOC entry 4743 (class 2606 OID 41280)
-- Name: producto producto_pkey1; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT producto_pkey1 PRIMARY KEY (id_prod);


--
-- TOC entry 4745 (class 2606 OID 41282)
-- Name: reembolso reembolso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reembolso
    ADD CONSTRAINT reembolso_pkey PRIMARY KEY (id_rem);


--
-- TOC entry 4747 (class 2606 OID 41284)
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id_usu);


--
-- TOC entry 4749 (class 2606 OID 41286)
-- Name: venta venta_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_pkey PRIMARY KEY (id_ven);


--
-- TOC entry 4750 (class 2606 OID 41287)
-- Name: detalle_venta detalle_venta_fk_id_ven_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detalle_venta
    ADD CONSTRAINT detalle_venta_fk_id_ven_fkey FOREIGN KEY (fk_id_ven) REFERENCES public.venta(id_ven);


--
-- TOC entry 4751 (class 2606 OID 41292)
-- Name: producto fk_categoria; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT fk_categoria FOREIGN KEY (prod_categoria) REFERENCES public.categoria(id_cat);


--
-- TOC entry 4752 (class 2606 OID 41297)
-- Name: reembolso reembolso_fk_id_ven_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reembolso
    ADD CONSTRAINT reembolso_fk_id_ven_fkey FOREIGN KEY (fk_id_ven) REFERENCES public.venta(id_ven);


--
-- TOC entry 4753 (class 2606 OID 41302)
-- Name: venta venta_fk_cliente; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.venta
    ADD CONSTRAINT venta_fk_cliente FOREIGN KEY (fk_id_cli) REFERENCES public.cliente(id_cli);


-- Completed on 2025-09-24 19:17:49

--
-- PostgreSQL database dump complete
--


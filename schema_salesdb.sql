--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

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
-- Name: sales_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sales_data (
    ordernumber integer,
    quantityordered integer,
    priceeach double precision,
    orderlinenumber integer,
    sales double precision,
    orderdate date,
    status character varying(50),
    qtr_id integer,
    month_id integer,
    year_id integer,
    productline character varying(100),
    msrp double precision,
    productcode character varying(50),
    customername character varying(150),
    phone character varying(100),
    addressline1 character varying(200),
    addressline2 character varying(200),
    city character varying(50),
    state character varying(50),
    postalcode character varying(20),
    country character varying(100),
    territory character varying(100),
    contactlastname character varying(100),
    contactfirstname character varying(100),
    dealsize character varying(20),
    paymentmethod character varying(100)
);


ALTER TABLE public.sales_data OWNER TO postgres;

--
-- PostgreSQL database dump complete
--


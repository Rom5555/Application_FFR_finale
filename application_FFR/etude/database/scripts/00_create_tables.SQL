-- object: new_database | type: DATABASE --
-- DROP DATABASE IF EXISTS new_database;
CREATE DATABASE new_database;
-- ddl-end --


-- object: public.produit | type: TABLE --
-- DROP TABLE IF EXISTS public.produit CASCADE;
CREATE TABLE public.produit (
	id_produit smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	nom_produit varchar(50),
	id_categorie_produit smallint,
	CONSTRAINT produit_pk PRIMARY KEY (id_produit),
	CONSTRAINT produit_unique UNIQUE (nom_produit)

);
-- ddl-end --
ALTER TABLE public.produit OWNER TO dev_role;
-- ddl-end --

-- object: public.categorie_produit | type: TABLE --
-- DROP TABLE IF EXISTS public.categorie_produit CASCADE;
CREATE TABLE public.categorie_produit (
	id_categorie_produit smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	nom_categorie_produit varchar(50),
	CONSTRAINT categorie_produit_pk PRIMARY KEY (id_categorie_produit)

);
-- ddl-end --
ALTER TABLE public.categorie_produit OWNER TO dev_role;
-- ddl-end --

-- object: categorie_produit_fk | type: CONSTRAINT --
-- ALTER TABLE public.produit DROP CONSTRAINT IF EXISTS categorie_produit_fk CASCADE;
ALTER TABLE public.produit ADD CONSTRAINT categorie_produit_fk FOREIGN KEY (id_categorie_produit)
REFERENCES public.categorie_produit (id_categorie_produit) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: public.stock | type: TABLE --
-- DROP TABLE IF EXISTS public.stock CASCADE;
CREATE TABLE public.stock (
	id_stock smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	nom_stock varchar(50),
	CONSTRAINT stock_pk PRIMARY KEY (id_stock),
	CONSTRAINT stock_unique UNIQUE (nom_stock)

);
-- ddl-end --
ALTER TABLE public.stock OWNER TO dev_role;
-- ddl-end --

-- object: public.liste_utilisateur | type: TABLE --
-- DROP TABLE IF EXISTS public.liste_utilisateur CASCADE;
CREATE TABLE public.liste_utilisateur (
	id_liste_utilisateur smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	id_utilisateur smallint,
	id_liste_depart smallint,
	date_liste date,
	destination varchar(30),
	en_cours boolean,
	CONSTRAINT liste_utilisateur_pk PRIMARY KEY (id_liste_utilisateur)

);
-- ddl-end --
ALTER TABLE public.liste_utilisateur OWNER TO dev_role;
-- ddl-end --

-- object: public.deplacement | type: TABLE --
-- DROP TABLE IF EXISTS public.deplacement CASCADE;
CREATE TABLE public.deplacement (
	id_deplacement smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	nombre_joueurs smallint,
	duree_deplacement smallint,
	nombre_match smallint,
	CONSTRAINT deplacement_pk PRIMARY KEY (id_deplacement),
	CONSTRAINT deplacement_unique UNIQUE (nombre_joueurs,duree_deplacement,nombre_match)

);
-- ddl-end --
ALTER TABLE public.deplacement OWNER TO dev_role;
-- ddl-end --

-- object: public.utilisateur | type: TABLE --
-- DROP TABLE IF EXISTS public.utilisateur CASCADE;
CREATE TABLE public.utilisateur (
	id_utilisateur smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	nom varchar(20),
	prenom varchar(20),
	mail varchar(30),
	mot_de_passe varchar(15),
	is_admin boolean,
	CONSTRAINT utilisateur_pk PRIMARY KEY (id_utilisateur),
	CONSTRAINT identifiant_utilisateur_unique UNIQUE (mail,mot_de_passe)

);
-- ddl-end --
ALTER TABLE public.utilisateur OWNER TO dev_role;
-- ddl-end --

-- object: public.association_stock_produit | type: TABLE --
-- DROP TABLE IF EXISTS public.association_stock_produit CASCADE;
CREATE TABLE public.association_stock_produit (
	id_association_stock_produit smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	id_stock smallint,
	id_produit smallint,
	quantite smallint,
	CONSTRAINT association_stock_produit_pk PRIMARY KEY (id_association_stock_produit)

);
-- ddl-end --
ALTER TABLE public.association_stock_produit OWNER TO dev_role;
-- ddl-end --

-- object: stock_fk | type: CONSTRAINT --
-- ALTER TABLE public.association_stock_produit DROP CONSTRAINT IF EXISTS stock_fk CASCADE;
ALTER TABLE public.association_stock_produit ADD CONSTRAINT stock_fk FOREIGN KEY (id_stock)
REFERENCES public.stock (id_stock) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: produit_fk | type: CONSTRAINT --
-- ALTER TABLE public.association_stock_produit DROP CONSTRAINT IF EXISTS produit_fk CASCADE;
ALTER TABLE public.association_stock_produit ADD CONSTRAINT produit_fk FOREIGN KEY (id_produit)
REFERENCES public.produit (id_produit) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: public.association_liste_utilisateur_produit | type: TABLE --
-- DROP TABLE IF EXISTS public.association_liste_utilisateur_produit CASCADE;
CREATE TABLE public.association_liste_utilisateur_produit (
	id_association_liste_utilisateur_produit smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	id_liste_utilisateur smallint,
	id_produit smallint,
	quantite_depart smallint,
	quantite_retour smallint,
	CONSTRAINT association_liste_utilisateur_produit_pk PRIMARY KEY (id_association_liste_utilisateur_produit)

);
-- ddl-end --
ALTER TABLE public.association_liste_utilisateur_produit OWNER TO dev_role;
-- ddl-end --

-- object: public.equipe | type: TABLE --
-- DROP TABLE IF EXISTS public.equipe CASCADE;
CREATE TABLE public.equipe (
	id_equipe smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	type_rugby smallint,
	genre varchar(10),
	categorie_age varchar(10),
	CONSTRAINT equipe_pk PRIMARY KEY (id_equipe)

);
-- ddl-end --
ALTER TABLE public.equipe OWNER TO dev_role;
-- ddl-end --

-- object: public.association_liste_depart_produit | type: TABLE --
-- DROP TABLE IF EXISTS public.association_liste_depart_produit CASCADE;
CREATE TABLE public.association_liste_depart_produit (
	id_association_liste_depart_produit smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	id_liste_depart smallint,
	id_produit smallint,
	quantite_depart smallint,
	quantite_retour smallint,
	CONSTRAINT association_liste_depart_produit_pk PRIMARY KEY (id_association_liste_depart_produit)

);
-- ddl-end --
ALTER TABLE public.association_liste_depart_produit OWNER TO dev_role;
-- ddl-end --

-- object: produit_fk | type: CONSTRAINT --
-- ALTER TABLE public.association_liste_depart_produit DROP CONSTRAINT IF EXISTS produit_fk CASCADE;
ALTER TABLE public.association_liste_depart_produit ADD CONSTRAINT produit_fk FOREIGN KEY (id_produit)
REFERENCES public.produit (id_produit) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: liste_utilisateur_fk | type: CONSTRAINT --
-- ALTER TABLE public.association_liste_utilisateur_produit DROP CONSTRAINT IF EXISTS liste_utilisateur_fk CASCADE;
ALTER TABLE public.association_liste_utilisateur_produit ADD CONSTRAINT liste_utilisateur_fk FOREIGN KEY (id_liste_utilisateur)
REFERENCES public.liste_utilisateur (id_liste_utilisateur) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: produit_fk | type: CONSTRAINT --
-- ALTER TABLE public.association_liste_utilisateur_produit DROP CONSTRAINT IF EXISTS produit_fk CASCADE;
ALTER TABLE public.association_liste_utilisateur_produit ADD CONSTRAINT produit_fk FOREIGN KEY (id_produit)
REFERENCES public.produit (id_produit) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: utilisateur_fk | type: CONSTRAINT --
-- ALTER TABLE public.liste_utilisateur DROP CONSTRAINT IF EXISTS utilisateur_fk CASCADE;
ALTER TABLE public.liste_utilisateur ADD CONSTRAINT utilisateur_fk FOREIGN KEY (id_utilisateur)
REFERENCES public.utilisateur (id_utilisateur) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: public.liste_depart | type: TABLE --
-- DROP TABLE IF EXISTS public.liste_depart CASCADE;
CREATE TABLE public.liste_depart (
	id_liste_depart smallint NOT NULL GENERATED ALWAYS AS IDENTITY ,
	id_deplacement smallint,
	id_equipe smallint,
	CONSTRAINT liste_depart_pk PRIMARY KEY (id_liste_depart)

);
-- ddl-end --
ALTER TABLE public.liste_depart OWNER TO dev_role;
-- ddl-end --

-- object: deplacement_fk | type: CONSTRAINT --
-- ALTER TABLE public.liste_depart DROP CONSTRAINT IF EXISTS deplacement_fk CASCADE;
ALTER TABLE public.liste_depart ADD CONSTRAINT deplacement_fk FOREIGN KEY (id_deplacement)
REFERENCES public.deplacement (id_deplacement) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: equipe_fk | type: CONSTRAINT --
-- ALTER TABLE public.liste_depart DROP CONSTRAINT IF EXISTS equipe_fk CASCADE;
ALTER TABLE public.liste_depart ADD CONSTRAINT equipe_fk FOREIGN KEY (id_equipe)
REFERENCES public.equipe (id_equipe) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: liste_depart_fk | type: CONSTRAINT --
-- ALTER TABLE public.liste_utilisateur DROP CONSTRAINT IF EXISTS liste_depart_fk CASCADE;
ALTER TABLE public.liste_utilisateur ADD CONSTRAINT liste_depart_fk FOREIGN KEY (id_liste_depart)
REFERENCES public.liste_depart (id_liste_depart) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: liste_depart_fk | type: CONSTRAINT --
-- ALTER TABLE public.association_liste_depart_produit DROP CONSTRAINT IF EXISTS liste_depart_fk CASCADE;
ALTER TABLE public.association_liste_depart_produit ADD CONSTRAINT liste_depart_fk FOREIGN KEY (id_liste_depart)
REFERENCES public.liste_depart (id_liste_depart) MATCH FULL
ON DELETE SET NULL ON UPDATE CASCADE;
-- ddl-end --

-- object: liste_depart_unique | type: CONSTRAINT --
-- ALTER TABLE public.liste_depart DROP CONSTRAINT IF EXISTS liste_depart_unique CASCADE;
ALTER TABLE public.liste_depart ADD CONSTRAINT liste_depart_unique UNIQUE (id_deplacement,id_equipe);
-- ddl-end --

-- object: association_liste_depart_produit_unique | type: CONSTRAINT --
-- ALTER TABLE public.association_liste_depart_produit DROP CONSTRAINT IF EXISTS association_liste_depart_produit_unique CASCADE;
ALTER TABLE public.association_liste_depart_produit ADD CONSTRAINT association_liste_depart_produit_unique UNIQUE (id_liste_depart,id_produit);
-- ddl-end --

-- object: association_liste_utilisateur_produit_unique | type: CONSTRAINT --
-- ALTER TABLE public.association_liste_utilisateur_produit DROP CONSTRAINT IF EXISTS association_liste_utilisateur_produit_unique CASCADE;
ALTER TABLE public.association_liste_utilisateur_produit ADD CONSTRAINT association_liste_utilisateur_produit_unique UNIQUE (id_liste_utilisateur,id_produit);
-- ddl-end --

-- object: liste_utilisateur_unique | type: CONSTRAINT --
-- ALTER TABLE public.liste_utilisateur DROP CONSTRAINT IF EXISTS liste_utilisateur_unique CASCADE;
ALTER TABLE public.liste_utilisateur ADD CONSTRAINT liste_utilisateur_unique UNIQUE (id_utilisateur,id_liste_depart,date_liste);
-- ddl-end --




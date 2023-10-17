/*1.- Se requiere listar los productos que tienen definido a cuál subcategoría pertenecen, 
omitir del listado aquellos que no cuentan con subcategoría, se necesita mostrar el productid, 
name, productnumber y productsubcategoryid.*/

SELECT p.productid, p.name, p.productnumber, p.productsubcategoryid
FROM public.product p
WHERE p.productsubcategoryid IS NOT NULL;

/*2.- Generar un listado con las cantidades de ordenes emitidas por cada año, considerar la fecha de emisión (orderdate).*/

SELECT EXTRACT(YEAR FROM orderdate)::DOUBLE PRECISION AS año, COUNT(*) AS cantidad_ordenes
FROM public.salesorderheader
GROUP BY año
ORDER BY año;

/*3.- Se necesita un reporte que muestre el listado de órdenes que cuentan con forma de pago con tarjeta vista, tener en consideración tablas 
creditcard y salesorderheader, se requieren los campos salesorderid, orderdate, duedate, shipdate, cardtype, cardnumber. */

SELECT so.salesorderid, so.orderdate, so.duedate, so.shipdate, cc.cardtype, cc.cardnumber
FROM public.salesorderheader so
INNER JOIN public.creditcard cc ON so.creditcardid = cc.creditcardid
WHERE cc.cardtype = 'Vista';
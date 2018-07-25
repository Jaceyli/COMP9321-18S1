**Contents**

[toc]
#Introduction
This documentation covers The Coffee Shop Order Service API (COMP9321 18S1 Assignment 1) designed by Jingxuan Li.

**Please test based the menu:**

|Name| Cost |
|---|---|
|Latte|3.5|
|Mocha|4|
|Cappuccino|4|
|Macchiato|3|
|Espresso|3.5|

**Description of status:**

|Status|Description|
|---|---|---|
|Placed|The order is created|
|Progressing| The coffee is in progress|
|Cancelled| The order has been Cancelled|

<br/>

---

#URLs and Operations

##Creating Order

| Operation | URL | Method | 
| --- | --- | --- | --- |
| CreateOrder | /Order | POST  |  

**Parameter**


| Field	| Type |	Description | Optional|Example|
| --- | --- | --- | --- | --- |
| coffee_tpye | String | coffee type |  |Latte |
|additions|String|additions demand (separated by ',')|N|skim,milk,extra shot|


**Returns**


<table>
<thead>
<tr>
<th>Status</th>
<th>Url</th>
<th>Return</th>
<th>Description</th>
</tr>
</thead>

<tbody>
<tr>
<td><font color=#5cb85c>201</font></td>
<td><font color=#5cb85c>POST</font>  <a href="http://127.0.0.1:5000/Order?coffee_type=Mocha">http://127.0.0.1:5000/Order?coffee_type=Mocha</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;coffee_type&quot;: &quot;Mocha&quot;,
    &quot;cost&quot;: 4,
    &quot;order_id&quot;: &quot;1521849765&quot;,
    &quot;payment&quot;: &quot;/payOrder/1521849765&quot;
}
</code>
</pre>
</td>

<td>
The order has been created successfully. The order_id is timestamp.
</td>
</tr>


<tr>
<td><font color=#d9534f>404</font></td>
<td><font color=#5cb85c>POST</font>  <a href="http://127.0.0.1:5000/Order?coffee_type=Orange">http://127.0.0.1:5000/Order?coffee_type=Orange</a></td>
<td>
<pre>
<code class="language-json">{
    &quot;coffee_type&quot;: &quot;false&quot;
}
</code>
</pre>
</td>

<td>
The type of coffee is not in the menu.
</td>
</tr>
</tbody>
</table>


<br/>

---


##Getting Order Details

| Operation | URL | Method | 
| --- | --- | --- | --- |
| Get one order details | /Order/&lt;id&gt;| GET |  

**Parameter**


| Field	| Type |	Description | Optional|Example|
| --- | --- | --- | --- | --- |
| id | String | order id |  | 1521849765 |


**Returns**


<table>
<thead>
<tr>
<th>Status</th>
<th>Url</th>
<th>Return</th>
<th>Description</th>
</tr>
</thead>

<tbody>
<tr>
<td><font color=#5cb85c>200</font></td>
<td><font color=#5cb85c>GET</font>  <a href="http://127.0.0.1:5000/Order/1521849765">http://127.0.0.1:5000/Order/1521849765</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;additions&quot;: [
        &quot;skim&quot;,
        &quot;milk&quot;,
        &quot;extra shot&quot;
    ],
    &quot;coffee_type&quot;: &quot;Mocha&quot;,
    &quot;order_id&quot;: &quot;1521849765&quot;,
    &quot;payment&quot;: &quot;/payOrder/1521849765&quot;
}
</code></pre>
</code>
</pre>
</td>

<td>
Getting order (<strong>not paid yet</strong>) details successfully.
</td>
</tr>


<tr>
<td><font color=#5cb85c>200</font></td>
<td><font color=#5cb85c>GET</font>  <a href="http://127.0.0.1:5000/Order/1521849765">http://127.0.0.1:5000/Order/1521849765</a></td>
<td>

<pre>
<code class="language-json">{
    &quot;additions&quot;: [
        &quot;skim&quot;,
        &quot;milk&quot;,
        &quot;extra shot&quot;
    ],
    &quot;coffee_type&quot;: &quot;Mocha&quot;,
    &quot;order_id&quot;: &quot;1521849765&quot;,
    &quot;payment&quot;: {
        &quot;card_info&quot;: &quot;1234567899&quot;,
        &quot;pay_time&quot;: &quot;Sat Mar 24 13:03:27 2018&quot;,
        &quot;pay_type&quot;: &quot;card&quot;
    }
}
</code>
</pre>
</td>

<td>
Getting order (<strong>already paid</strong>) details successfully.
</td>
</tr>

<tr>
<td><font color=#d9534f>404</font></td>
<td><font color=#5cb85c>GET</font>  <a href="http://127.0.0.1:5000/Order/0
">http://127.0.0.1:5000/Order/0
</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;coffee_type&quot;: &quot;false&quot;
}
</code>
</pre>
</td>

<td>
The order id is not found.
</td>
</tr>
</tbody>
</table>


<br/>

---

##Getting List of all Open Orders


| Operation | URL | Method | 
| --- | --- | --- | --- |
| Get all open order details | /OpenOrders | GET |  

**Parameter**

None


**Returns**


<table>
<thead>
<tr>
<th>Status</th>
<th>Url</th>
<th>Return</th>
<th>Description</th>
</tr>
</thead>

<tbody>
<tr>
<td><font color=#5cb85c>200</font></td>
<td><font color=#5cb85c>GET</font>  <a href="http://127.0.0.1:5000/OpenOrders">http://127.0.0.1:5000/OpenOrders</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;result&quot;: [
        {
            &quot;additions&quot;: null,
            &quot;coffee_type&quot;: &quot;Latte&quot;,
            &quot;cost&quot;: 3.5,
            &quot;order_id&quot;: &quot;1521858089&quot;,
            &quot;payment&quot;: &quot;F&quot;,
            &quot;status&quot;: &quot;Placed&quot;
        },
        {
            &quot;additions&quot;: [
                &quot;add suger&quot;
            ],
            &quot;coffee_type&quot;: &quot;Mocha&quot;,
            &quot;cost&quot;: 4,
            &quot;order_id&quot;: &quot;1521858132&quot;,
            &quot;payment&quot;: &quot;F&quot;,
            &quot;status&quot;: &quot;Progressing&quot;
        }
    ],
    &quot;resultSize&quot;: 2
}
</code>
</pre>
</td>

<td>
Get all the open orders's details successfully.
</td>
</tr>
</tbody>
</table>

<br/>

---

##Amending Order

###Amending order details (by cashier)


| Operation | URL | Method | 
| --- | --- | --- | --- |
| Amend order details by cashier| /Order/&lt;id&gt;| PUT |  

* *The order only can be amended before paying and progressing*

**Parameter**


| Field	| Type |	Description | Optional|Example|
| --- | --- | --- | --- | --- |
| id | String | order id |  | 1521849765 |
| coffee_tpye | String | coffee type |  |Latte |
|additions|String|additions demand (separated by ',')| Y |skim,milk,extra shot|


**Returns**


<table>
<thead>
<tr>
<th>Status</th>
<th>Url</th>
<th>Return</th>
<th>Description</th>
</tr>
</thead>

<tbody>

<tr>
<td><font color=#5cb85c>100</font></td>
<td><font color=#5cb85c>PUT</font>  <a href="http://127.0.0.1:5000/Order/1521858089">http://127.0.0.1:5000/Order/1521858089</a></td>
<td>
</td>
<td>
The order can be amended. Please continue.
</td>
</tr>

<tr>
<td><font color=#d9534f>417</font></td>
<td><font color=#5cb85c>PUT</font>  <a href="http://127.0.0.1:5000/Order/1521858089">http://127.0.0.1:5000/Order/1521858089</a></td>
<td>
<pre>
<code class="language-json">{
    &quot;error&quot;: &quot;The order can not be changed.&quot;
}
</code></pre>
</td>
<td>
The order can not be amended. It has paid or in progressing.
</td>
</tr>

<tr>
<td><font color=#5cb85c>200</font></td>
<td><font color=#5cb85c>PUT</font>  <a href="http://127.0.0.1:5000/Order/1521858089?coffee_type=Mocha&additions=skim,milk,extra shot">http://127.0.0.1:5000/Order/1521858089?coffee_type=Mocha&additions=skim,milk,extra shot</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;additions&quot;: [
        &quot;skim&quot;,
        &quot;milk&quot;,
        &quot;extra shot&quot;
    ],
    &quot;coffee_type&quot;: &quot;Mocha&quot;,
    &quot;cost&quot;: 4,
    &quot;order_id&quot;: &quot;1521858089&quot;
}
</code></pre>
</code>
</pre>
</td>

<td>
 Add additions successfully.
</td>
</tr>


<tr>
<td><font color=#d9534f>409</font></td>
<td><font color=#5cb85c>PUT</font>  <a href="http://127.0.0.1:5000/Order/1521858089?coffee_type=Mocha&additions=skim,milk,extra shot">http://127.0.0.1:5000/Order/1521858089?coffee_type=Mocha&additions=skim,milk,extra shot</a></td>
<td>
<pre>
<code class="language-json">{
    &quot;error&quot;: &quot;The order can not be changed.&quot;
}
</code>
</pre>
</td>

<td>
The order can not be amended. It has been paid or in progressing.
</td>
</tr>

<tr>
<td><font color=#d9534f>404</font></td>
<td><font color=#5cb85c>PUT</font>  <a href="http://127.0.0.1:5000/Order/0?coffee_type=Mocha&additions=skim,milk,extra shot">http://127.0.0.1:5000/Order/0?coffee_type=Mocha&additions=skim,milk,extra shot</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;order_id&quot;: &quot;false&quot;
}
</code>
</pre>
</td>

<td>
The order id is not found.
</td>
</tr>

</tbody>
</table>

<br/>

###Amending order status (by barista)



| Operation | URL | Method | 
| --- | --- | --- | --- |
| Amend status by barista | /Order/&lt;id&gt;| PATCH |  


**Parameter**


| Field	| Type |	Description | Optional |Example|
| --- | --- | --- | --- | --- |
| status | String | amend status to "Progressing" or "Cancelled"|  | Progressing |

* *The order only can be amended to "progressing" when it is placed*
* *The order can not be cancelled after payment*


**Returns**


<table>
<thead>
<tr>
<th>Status</th>
<th>Url</th>
<th>Return</th>
<th>Description</th>
</tr>
</thead>

<tbody>
<tr>
<td><font color=#5cb85c>200</font></td>
<td><font color=#5cb85c>PATCH</font>  <a href="http://127.0.0.1:5000/Order/1521870828?status=Progressing">http://127.0.0.1:5000/Order/1521870828?status=Progressing</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;order_id&quot;: &quot;1521870828&quot;,
    &quot;status&quot;: &quot;Progressing&quot;
}
</code>
</pre>
</td>
<td>
The order has amended to "Progressing" successfully.
</td>
</tr>

<tr>
<td><font color=#d9534f>409</font></td>
<td><font color=#5cb85c>PATCH</font>  <a http://127.0.0.1:5000/Order/1521872503?status=Cancelled">http://127.0.0.1:5000/Order/1521872503?status=Cancelled</a></td>
<td>
<pre>
<code class="language-json">{
    &quot;error&quot;: &quot;The order can not be cancelled&quot;
    <!--The order can not be cancelled after payment!-->
}
</code></pre>
</code>
</pre>
</td>

<td>
The order can not be cancelled. It has been paid.</td>
</tr>


<tr>
<td><font color=#d9534f>409</font></td>
<td><font color=#5cb85c>PATCH</font>  <a href="http://127.0.0.1:5000/Order/1521870828?status=Progressing">http://127.0.0.1:5000/Order/1521870828?status=Progressing</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;error&quot;: &quot;The order has been progressing.&quot;
}
</code></pre>
</code>
</pre>
</td>

<td>
The order has been progressing.
</td>
</tr>

<tr>
<td><font color=#d9534f>409</font></td>
<td><font color=#5cb85c>PATCH</font>  <a href="http://127.0.0.1:5000/Order/1521870828?status=Cancelled">http://127.0.0.1:5000/Order/1521870828?status=Cancelled</a></td>
<td>
<pre>
<code class="language-json">{
    &quot;error&quot;: &quot;The order has been cancelled.&quot;
}
</code></pre>
</code>
</pre>
</td>

<td>
The order has been cancelled.
</td>
</tr>


<tr>
<td><font color=#d9534f>404</font></td>
<td><font color=#5cb85c>PATCH</font>  <a href="http://127.0.0.1:5000/Order/1521872503?status=1">http://127.0.0.1:5000/Order/1521872503?status=1</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;error&quot;: &quot;Wrong status!&quot;
}
</code></pre>
</code>
</pre>
</td>

<td>
The status should be "Progressing" or "Cancelled".
</td>
</tr>


<tr>
<td><font color=#d9534f>404</font></td>
<td><font color=#5cb85c>PATCH</font>  <a href="http://127.0.0.1:5000/Order/1?status=Progressing">http://127.0.0.1:5000/Order/1?status=Progressing</a></td>
<td>
<pre>
<code class="language-json">{
    &quot;order_id&quot;: &quot;false&quot;
}
</code>
</pre>
</td>

<td>
The order id is not found.
</td>
</tr>


</tbody>
</table>






<br/>

---


##Getting Orders List


| Operation | URL | Method | 
| --- | --- | --- | --- |
| Get all order details | /Orders | GET |  

**Parameter**

None


**Returns**


<table>
<thead>
<tr>
<th>Status</th>
<th>Url</th>
<th>Return</th>
<th>Description</th>
</tr>
</thead>

<tbody>
<tr>
<td><font color=#5cb85c>200</font></td>
<td><font color=#5cb85c>GET</font>  <a href="http://127.0.0.1:5000/Orders">http://127.0.0.1:5000/Orders</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;result&quot;: [
    {
        &quot;additions&quot;: null,
        &quot;coffee_type&quot;: &quot;Latte&quot;,
        &quot;cost&quot;: 3.5,
        &quot;order_id&quot;: &quot;1521874827&quot;,
        &quot;payment&quot;: &quot;F&quot;,
        &quot;status&quot;: &quot;Cancelled&quot;
    },
    {
        &quot;additions&quot;: [
            &quot;add suger&quot;
        ],
        &quot;coffee_type&quot;: &quot;Mocha&quot;,
        &quot;cost&quot;: 4,
        &quot;order_id&quot;: &quot;1521874829&quot;,
        &quot;payment&quot;: &quot;F&quot;,
        &quot;status&quot;: &quot;Progressing&quot;
    },
    {
        &quot;additions&quot;: null,
        &quot;coffee_type&quot;: &quot;Cappuccino&quot;,
        &quot;cost&quot;: 4,
        &quot;order_id&quot;: &quot;1521874831&quot;,
        &quot;payment&quot;: &quot;F&quot;,
        &quot;status&quot;: &quot;Placed&quot;
    }
],
&quot;resultSize&quot;: 3
}
</code>
</pre>
</td>

<td>
Get all the orders list successfully.
</td>
</tr>
</tbody>
</table>

<br/>

---

		
##Creating a Payment


| Operation | URL | Method | 
| --- | --- | --- | --- |
|Create a payment | /payment/&lt;id&gt; | PUT  |  

**Parameter**


| Field	| Type |	Description | Optional|Example|
| --- | --- | --- | --- | --- |
| pay_type | String | card&cash |  |card |
|amount|int|order cost |  |4|
|card_info|String| card number| Y | 123456789|


**Returns**


<table>
<thead>
<tr>
<th>Status</th>
<th>Url</th>
<th>Return</th>
<th>Description</th>
</tr>
</thead>

<tbody>
<tr>
<td><font color=#5cb85c>201</font></td>
<td><font color=#5cb85c>PUT</font>  <a href="http://127.0.0.1:5000/payment/1521849765?pay_type=card&amount=4&card_info=1234567899">http://127.0.0.1:5000/payment/1521849765?pay_type=card&amount=4&card_info=1234567899</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;amount&quot;: 4,
    &quot;card_info&quot;: &quot;1234567899&quot;,
    &quot;order_id&quot;: &quot;1521849765&quot;,
    &quot;pay_time&quot;: &quot;Sat Mar 24 13:03:27 2018&quot;,
    &quot;pay_type&quot;: &quot;card&quot;
}
</code>
</pre>
</td>

<td>
The order has been paid by card successfully.</td>
</tr>

<tr>
<td><font color=#5cb85c>201</font></td>
<td><font color=#5cb85c>PUT</font>  <a href="http://127.0.0.1:5000/payment/1521874829?pay_type=cash&amount=4">http://127.0.0.1:5000/payment/1521874829?pay_type=cash&amount=4</a></td>
<td>
<pre>
<code class="language-json">{
    &quot;amount&quot;: 4,
    &quot;order_id&quot;: &quot;1521874829&quot;,
    &quot;pay_time&quot;: &quot;Sat Mar 24 18:13:54 2018&quot;,
    &quot;pay_type&quot;: &quot;cash&quot;
}
</code>
</pre>
</td>

<td>
The order has been paid by cash successfully.</td>
</tr>


<tr>
<td><font color=#d9534f>409</font></td>
<td><font color=#5cb85c>PUT</font>  <a href="http://127.0.0.1:5000/payment/1521874829?pay_type=cash&amount=4">http://127.0.0.1:5000/payment/1521874829?pay_type=cash&amount=4</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;error&quot;: &quot;You already paid for your coffee.&quot;
}
</code>
</pre>
</td>

<td>
You paid your order again.
</td>
</tr>

<tr>
<td><font color=#d9534f>409</font></td>
<td><font color=#5cb85c>PUT</font>  <a href="http://127.0.0.1:5000/payment/1521876102?pay_type=cash&amount=3.5">http://127.0.0.1:5000/payment/1521876102?pay_type=cash&amount=3.5</a></td>
<td>
<pre>
<code class="language-json">{
    &quot;error&quot;: &quot;You order has been cancelled.&quot;
}
</code>
</pre>
</td>

<td>
You order has been cancelled.
</td>
</tr>

<tr>
<td><font color=#d9534f>400</font></td>
<td><font color=#5cb85c>PUT</font>  <a href="http://127.0.0.1:5000/payment/1521876202?pay_type=cash&amount=3.5">http://127.0.0.1:5000/payment/1521876202?pay_type=cash&amount=3.5</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;error&quot;: &quot;Sorry. The cost is not correct.&quot;
}
</code>
</pre>
</td>

<td>
The amount you paid is not same to your order cost.
</td>
</tr>

<tr>
<td><font color=#d9534f>400</font></td>
<td><font color=#5cb85c>PUT</font>  <a href="http://127.0.0.1:5000/payment/1521876202?pay_type=1&amount=3.5">http://127.0.0.1:5000/payment/1521876202?pay_type=1&amount=3.5</a></td>
<td>
<pre>
<code class="language-json">{
    &quot;error&quot;: &quot;Wrong payment type. (card or cash)&quot;
}
</code>
</pre>
</td>

<td>
The amount you paid is not same to your order cost.
</td>
</tr>

<tr>
<td><font color=#d9534f>404</font></td>
<td><font color=#5cb85c>PUT</font>  <a href="http://127.0.0.1:5000/payment/1?pay_type=cash&amount=3.5">http://127.0.0.1:5000/payment/1?pay_type=cash&amount=3.5</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;coffee_type&quot;: &quot;false&quot;
}
</code>
</pre>
</td>

<td>
The order id is not found.
</td>
</tr>

</tbody>
</table>


<br/>

---

##Getting Payment Details for an Order 



| Operation | URL | Method | 
| --- | --- | --- | --- |
| Get one order payment details | /payment/&lt;id&gt;| GET |  

**Parameter**


| Field	| Type |	Description | Optional|Example|
| --- | --- | --- | --- | --- |
| id | String | order id |  | 1521849765 |


**Returns**


<table>
<thead>
<tr>
<th>Status</th>
<th>Url</th>
<th>Return</th>
<th>Description</th>
</tr>
</thead>

<tbody>
<tr>
<td><font color=#5cb85c>200</font></td>
<td><font color=#5cb85c>GET</font>  <a href="http://127.0.0.1:5000/payment/1521876202">http://127.0.0.1:5000/payment/1521876202</a></td>
<td>
<pre style="background: #FFFFFF">
<code class="language-json">{
    &quot;amount&quot;: 4,
    &quot;card_info&quot;: &quot;1234567899&quot;,
    &quot;order_id&quot;: &quot;1521876202&quot;,
    &quot;pay_time&quot;: &quot;Sat Mar 24 18:35:22 2018&quot;,
    &quot;pay_type&quot;: &quot;card&quot;
}
</code></pre>
</code>
</pre>
</td>

<td>
Get the payment details successfully.
</td>
</tr>

<tr>
<td><font color=#d9534f>404</font></td>
<td><font color=#5cb85c>GET</font>  <a href="http://127.0.0.1:5000/payment/1521876202">http://127.0.0.1:5000/payment/1521876202</a></td>
<td>
<pre>
<code class="language-json">{
    &quot;error&quot;: &quot;The order 1521876202 has not paid yet.&quot;
}
</code></pre>
</code>
</pre>
</td>

<td>
The order has not paid yet.
</td>
</tr>


</tbody>
</table>


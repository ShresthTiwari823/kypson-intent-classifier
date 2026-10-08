# Note
The keyword baseline checks keywords, so sometimes it gives the wrong intent when the message has more than one thing.

### 1.
Message: `don't show my orders, what's a fair price`

Baseline: `data_query`
My classifier: `price_intel`
The baseline sees "orders", but the user is asking about the price.

### 2.
Message: `food grade laminate ke liye supplier batao`

Baseline: `spec_help`
My classifier: `supplier_rec`
The user is asking for a supplier, not asking what food grade means.

### 3.
Message: `50 gsm bags ke liye RFQ likh do`

Baseline: `spec_help`
My classifier: `rfq_assist`
The message has "50 gsm", but the main request is to write an RFQ.

### 4.
Message: `order page kahan hai`

Baseline: `data_query`
My classifier: `navigation`
The user wants to know where the order page is.

### 5.
Message: `not the price, show my quotations`

Baseline: `price_intel`
My classifier: `data_query`
The baseline sees "price", but the user is asking to see quotations.
Overall, the main difference is that my classifier tries to understand the actual request instead of only checking keywords.


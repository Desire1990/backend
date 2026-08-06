import{M as I}from"./Modal-DryBCHCe.js";import{_ as N,o as i,j as P,w as R,a as t,n as f,c as r,t as n,h as o,H as v,f as m,F as x,s as w,I as $,q as d,y as p,G as S,g as b,z as B}from"./index-DSBCjaMJ.js";const E={class:"receipt-container"},D={class:"format-toggle"},F={class:"preview-area"},M={class:"thermal-content"},j={class:"text-center"},q={key:0},H={key:1},L={class:"thermal-table"},O={class:"text-right"},G={class:"text-right"},z={class:"text-right"},V={class:"thermal-total"},W={class:"text-center"},K={class:"a4-content"},Q={class:"a4-title"},Y={class:"a4-info-grid"},U={class:"a4-table"},J={class:"text-right"},X={class:"text-right"},Z={class:"text-right"},_={class:"a4-totals"},tt={class:"a4-total-row"},lt={class:"a4-total-row"},et={class:"a4-total-row grand-total"},nt={class:"receipt-actions"},st={__name:"ReceiptBill",props:{show:Boolean,sale:Object},emits:["close"],setup(s,{emit:at}){const k=s,a=b("thermal"),c=b(null),h=b(null),T=B(()=>{var u,l;return((l=(u=k.sale)==null?void 0:u.items)==null?void 0:l.reduce((e,y)=>e+y.quantity,0))||0});function A(){const l=(a.value==="thermal"?c:h).value.innerHTML,e=window.open("","_blank");e.document.write(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>Print Receipt</title>
        <style>
          @page {
            size: ${a.value==="thermal"?"80mm auto":"A4"};
            margin: ${a.value==="thermal"?"0mm":"10mm"};
          }
          body {
            font-family: ${a.value==="thermal"?"'Courier New', monospace":"'Arial', sans-serif"};
            margin: 0;
            padding: ${a.value==="thermal"?"5mm":"0"};
          }
          ${g()}
        </style>
      </head>
      <body>
        ${l}
        <script>
          window.onload = () => {
            window.print();
            setTimeout(() => window.close(), 500);
          }
        <\/script>
      </body>
    </html>
  `),e.document.close()}function g(){return`
    .thermal-content { max-width: 80mm; margin: 0 auto; }
    .dashed-line { border-top: 1px dashed #000; margin: 5px 0; }
    .text-center { text-align: center; }
    .text-right { text-align: right; }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 2px 4px; }
    th { border-bottom: 1px solid #000; }
    .a4-content { padding: 20px; }
    .a4-header { display: flex; justify-content: space-between; }
    .a4-table th, .a4-table td { border: 1px solid #000; padding: 5px; }
    .a4-totals { margin-left: auto; width: 300px; }
    .a4-total-row { display: flex; justify-content: space-between; padding: 5px; }
    .grand-total { font-weight: bold; font-size: 1.2em; border-top: 2px solid #000; }
    .a4-signatures { display: flex; justify-content: space-between; margin-top: 50px; }
    .signature-line { border-top: 1px solid #000; width: 200px; margin-bottom: 5px; }
    @media print {
      .receipt-actions, .format-toggle { display: none !important; }
    }
  `}function C(){const l=(a.value==="thermal"?c:h).value.innerHTML,e=window.open("","_blank");e.document.write(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>Receipt</title>
        <style>
          body { font-family: Arial, sans-serif; }
          ${g()}
        </style>
      </head>
      <body>${l}</body>
    </html>
  `),e.document.close(),e.print()}return(u,l)=>s.sale?(i(),P(I,{key:0,show:s.show,onClose:l[3]||(l[3]=e=>u.$emit("close"))},{default:R(()=>[t("div",E,[t("div",D,[t("button",{class:f(["btn",a.value==="thermal"?"btn-primary":"btn-outline"]),onClick:l[0]||(l[0]=e=>a.value="thermal")}," 🧾 Thermal (80mm) ",2),t("button",{class:f(["btn",a.value==="a4"?"btn-primary":"btn-outline"]),onClick:l[1]||(l[1]=e=>a.value="a4")}," 📄 A4 Format ",2)]),t("div",F,[a.value==="thermal"?(i(),r("div",{key:0,class:"thermal-receipt",ref_key:"thermalRef",ref:c},[t("div",M,[t("div",j,[l[4]||(l[4]=t("h3",null,"💊 SHIMA PHAR",-1)),l[5]||(l[5]=t("p",null,"1 Gisyo, Kanyosha-Bujumbura",-1)),l[6]||(l[6]=t("p",null,"Tel: +257 79 462 806",-1)),l[7]||(l[7]=t("p",null,"Email: info@shimaphar.bi",-1)),l[8]||(l[8]=t("p",null,"NIF/TIN: 4001462136",-1)),l[9]||(l[9]=t("div",{class:"dashed-line"},null,-1)),l[10]||(l[10]=t("p",null,[t("strong",null,"SALE RECEIPT")],-1)),t("p",null,"No: #"+n(s.sale.id),1),t("p",null,n(o(v)(s.sale.created_at)),1),s.sale.customer_name?(i(),r("p",q,"Customer: "+n(s.sale.customer_name),1)):m("",!0),s.sale.user_name?(i(),r("p",H,"Served by: "+n(s.sale.user_name),1)):m("",!0),l[11]||(l[11]=t("div",{class:"dashed-line"},null,-1))]),t("table",L,[l[12]||(l[12]=t("thead",null,[t("tr",null,[t("th",null,"Item"),t("th",{class:"text-right"},"Qty"),t("th",{class:"text-right"},"Price"),t("th",{class:"text-right"},"Amount")])],-1)),t("tbody",null,[(i(!0),r(x,null,w(s.sale.items,e=>(i(),r("tr",{key:e.id},[t("td",null,n(o($)(e.medicine_name,15)),1),t("td",O,n(e.quantity),1),t("td",G,n(o(d)(e.price)),1),t("td",z,n(o(d)(e.price*e.quantity)),1)]))),128))])]),l[15]||(l[15]=t("div",{class:"dashed-line"},null,-1)),t("div",V,[t("span",null,"Total Items: "+n(T.value),1),t("span",null,"TOTAL: "+n(o(d)(s.sale.total)),1)]),l[16]||(l[16]=t("div",{class:"dashed-line"},null,-1)),t("div",W,[l[13]||(l[13]=t("p",null,"Thank you for your purchase!",-1)),l[14]||(l[14]=t("p",null,"Goods once sold cannot be returned",-1)),t("p",null,n(o(v)(new Date)),1)])])],512)):m("",!0),a.value==="a4"?(i(),r("div",{key:1,class:"a4-receipt",ref_key:"a4Ref",ref:h},[t("div",K,[l[26]||(l[26]=t("div",{class:"a4-header"},[t("div",{class:"a4-logo"},[t("h1",null,"💊 SHIMA PHAR"),t("p",null,"Pharmacy Management System")]),t("div",{class:"a4-company-info"},[t("p",null,"1 Gisyo, Kanyosha-Bujumbura"),t("p",null,"Tel: +257 79 462 806"),t("p",null,"Email: info@shimaphar.bi"),t("p",null,"NIF/TIN: 4001462136")])],-1)),t("div",Q,[l[17]||(l[17]=t("h2",null,"SALE INVOICE",-1)),t("p",null,"Invoice #"+n(s.sale.id),1)]),t("div",Y,[t("div",null,[l[18]||(l[18]=t("strong",null,"Date:",-1)),p(" "+n(o(v)(s.sale.created_at)),1)]),t("div",null,[l[19]||(l[19]=t("strong",null,"Customer:",-1)),p(" "+n(s.sale.customer_name||"Walk-in Customer"),1)]),t("div",null,[l[20]||(l[20]=t("strong",null,"Served By:",-1)),p(" "+n(s.sale.user_name||"N/A"),1)]),l[21]||(l[21]=t("div",null,[t("strong",null,"Payment Method:"),p(" Cash ")],-1))]),t("table",U,[l[22]||(l[22]=t("thead",null,[t("tr",null,[t("th",null,"#"),t("th",null,"Medicine"),t("th",null,"Batch"),t("th",null,"Expiry"),t("th",{class:"text-right"},"Qty"),t("th",{class:"text-right"},"Unit Price"),t("th",{class:"text-right"},"Amount")])],-1)),t("tbody",null,[(i(!0),r(x,null,w(s.sale.items,(e,y)=>(i(),r("tr",{key:e.id},[t("td",null,n(y+1),1),t("td",null,n(e.medicine_name),1),t("td",null,n(e.batch_number||"N/A"),1),t("td",null,n(e.expiry_date?o(S)(e.expiry_date):"N/A"),1),t("td",J,n(e.quantity),1),t("td",X,n(o(d)(e.price)),1),t("td",Z,n(o(d)(e.price*e.quantity)),1)]))),128))])]),t("div",_,[t("div",tt,[l[23]||(l[23]=t("span",null,"Subtotal:",-1)),t("span",null,n(o(d)(s.sale.total)),1)]),t("div",lt,[l[24]||(l[24]=t("span",null,"Tax (VAT 18%):",-1)),t("span",null,n(o(d)(s.sale.total*.18)),1)]),t("div",et,[l[25]||(l[25]=t("span",null,"GRAND TOTAL:",-1)),t("span",null,n(o(d)(s.sale.total*1.18)),1)])]),l[27]||(l[27]=t("div",{class:"a4-footer"},[t("p",null,"Thank you for your purchase!"),t("p",null,"Goods once sold cannot be returned."),t("p",null,"For any queries, please contact us at +257 79 462 806")],-1)),l[28]||(l[28]=t("div",{class:"a4-signatures"},[t("div",null,[t("div",{class:"signature-line"}),t("p",null,"Customer Signature")]),t("div",null,[t("div",{class:"signature-line"}),t("p",null,"Authorized Signature")])],-1))])],512)):m("",!0)]),t("div",nt,[t("button",{class:"btn btn-secondary",onClick:l[2]||(l[2]=e=>u.$emit("close"))}," ❌ Close "),t("button",{class:"btn btn-primary",onClick:A}," 🖨️ Print "+n(a.value==="thermal"?"Thermal":"A4"),1),t("button",{class:"btn btn-success",onClick:C}," 📥 Download PDF ")])])]),_:1},8,["show"])):m("",!0)}},rt=N(st,[["__scopeId","data-v-d885b25e"]]);export{rt as R};

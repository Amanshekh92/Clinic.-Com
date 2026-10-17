(()=>{"use strict";
const HI={};
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
let lang="en";
const t=s=>lang==="hi"&&HI[s]||s,dg=s=>String(s||"").replace(/\D/g,"");
const el=(g,x,c)=>{const e=document.createElement(g);if(x!=null)e.textContent=x;if(c)e.className=c;return e};
const toast=m=>{const x=$("#toast");x.textContent=m;x.classList.add("on");clearTimeout(toast.i);toast.i=setTimeout(()=>x.classList.remove("on"),4500)};
const today=()=>new Date(Date.now()-new Date().getTimezoneOffset()*6e4).toISOString().slice(0,10);
const waNum=()=>{let d=dg(C.whatsapp).replace(/^00/,"");if(/^[6-9]\d{9}$/.test(d))d="91"+d;return /^\d{11,15}$/.test(d)?d:""};
const waBase=()=>waNum()?"https://wa.me/"+waNum():"";
const safe=u=>{try{const x=new URL(u);return x.protocol==="https:"?x.href:""}catch(e){return ""}};
const telHref=()=>{let d=dg(C.phone);if(/^[6-9]\d{9}$/.test(d))d="91"+d;else if(/^0\d{10}$/.test(d))d="91"+d.slice(1);return d.length>=11&&d.length<=15?"tel:+"+d:""};
const safeEmbed=u=>{const s=safe(u);if(!s)return "";const x=new URL(s);return /^(www\.google\.(com|co\.in)|maps\.google\.com)$/.test(x.hostname)&&x.pathname.startsWith("/maps")?s:""};
const mailOk=()=>/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(C.email||"");
const dayName=d=>{const h=C.hours.find(x=>x.d[0]===d);return h?h.d[lang==="hi"?1:0]:d};
const phoneTxt=()=>{const h=telHref().replace("tel:+","");return h.length===12&&h.startsWith("91")?"+91 "+h.slice(2,7)+" "+h.slice(7):C.phone};
const ratingTxt=()=>{const r=C.rating;return r&&r.score?Number(r.score).toFixed(1)+" ★ · "+r.count+" "+t("Google reviews")+" · "+t("as of")+" "+r.asof:""};
const hoursTxt=()=>{const o=C.hours.filter(h=>h.t&&h.t!=="Closed");if(!o.length||!o.every(h=>h.t===o[0].t))return "";return t(o[0].t)+(C.holidays?" · "+t("Closed")+": "+dayName(C.holidays):"")};
const openUrl=u=>{try{const a=document.createElement("a");a.href=u;a.target="_blank";a.rel="noopener noreferrer";a.style.display="none";document.body.append(a);a.click();a.remove()}catch(e){if(!window.open(u,"_blank"))location.href=u}};
const IMG={rct:'root-canal',braces:'braces-aligners',gum:'gum-care'};
const nm=s=>s[lang==="hi"?"hi":"en"];
let cat="All",q="",data=null,last={k:"",a:0},waUrl="",infoKind="faq",first=true;
const SCR=["home","svc","book","doc","appt","rev","prof","more","info"],PARENT={svc:"home",appt:"home",prof:"home",book:"svc",doc:"prof",rev:"prof",more:"prof",info:"more"};
const route=()=>{const h=location.hash.replace(/^#\/?/,"").split("/");const n=SCR.includes(h[0])?h[0]:"home";if(n==="info")infoKind=["hours","faq","privacy","terms"].includes(h[1])?h[1]:"faq";return n};
function go(n,k){const h="#/"+n+(k?"/"+k:"");if(location.hash===h)show(n);else location.hash=h}
function show(n){
 $$(".scr").forEach(s=>s.classList.toggle("on",s.id==="s-"+n));scrollTo(0,0);
 const cur=n==="book"?"svc":(n==="more"||n==="doc"||n==="rev"||n==="info")?"prof":n;
 $$("nav button").forEach(b=>b.dataset.go===cur?b.setAttribute("aria-current","page"):b.removeAttribute("aria-current"));
 if(n==="book")step(1);if(n==="info")renderInfo();
 if(!first){const h=$("#s-"+n+" h1");if(h){h.tabIndex=-1;h.focus({preventScroll:true})}}first=false}
addEventListener("hashchange",()=>show(route()));
function step(n){$("#bf").hidden=n!==1;$("#b2").hidden=n!==2;$("#b3").hidden=n!==3;
 $$("#steps span").forEach((s,i)=>s.classList.toggle("cur",i===n-1));}
function render(){
 document.documentElement.lang=lang;
 $$("[data-t]").forEach(n=>n.textContent=t(n.dataset.t));
 $$("[data-tp]").forEach(n=>n.placeholder=t(n.dataset.tp));
 $$(".cn").forEach(n=>n.textContent=C.name);
 $("#demo").hidden=true;
 $$(".langbtn").forEach(b=>{b.hidden=true});$("#lg").hidden=true;
 const vis=C.svc.filter(s=>s.ok||C.demo);
 const ch=$("#chips");ch.replaceChildren();
 ["All","General","Cosmetic","Kids","Advanced"].forEach(c=>{const b=el("button",t(c),"chip");b.type="button";b.setAttribute("aria-pressed",String(c===cat));b.onclick=()=>{cat=c;render()};ch.append(b)});
 const tl=$("#tl");tl.replaceChildren();const qq=q.toLowerCase();let n=0;
 const cols={General:["#d9f1f2","#a9dfe2"],Advanced:["#dde8f7","#b5cdee"],Cosmetic:["#f6e3f1","#e8bfdc"],Kids:["#e3f5e0","#bfe6b8"]};
 vis.forEach(s=>{ if(cat!=="All"&&s.c!==cat)return; if(qq&&!(s.en+s.hi).toLowerCase().includes(qq))return; n++;
  const b=el("button",null,"card");b.type="button";b.dataset.book=s.id;
  const ph=el("div",null,"ph");ph.style.background=`linear-gradient(135deg,${cols[s.c][0]},${cols[s.c][1]})`;
  const i=el("img");i.src="treatment-"+(IMG[s.id]||s.id)+".webp";i.alt=nm(s)+" (sample illustration)";i.width=600;i.height=400;i.loading="lazy";ph.append(i)
  const tx=el("div"),bb=el("b",nm(s));if(!s.ok)bb.append(el("span",t("Sample"),"tag"));tx.append(bb,el("small",lang==="hi"?s.dh:s.de));
  b.append(ph,tx);tl.append(b)});
 $("#none").hidden=n>0;
 const sel=$("#f-tr"),k=sel.value;sel.replaceChildren(new Option(t("Choose treatment"),""));vis.forEach(s=>sel.append(new Option(nm(s),s.id)));sel.value=k;
 const tm=$("#f-time"),tk=tm.value||"0";tm.replaceChildren();["Any time","Morning","Afternoon","Evening"].forEach((x,i)=>tm.append(new Option(t(x),String(i))));tm.value=tk;
 const dl=$("#dl");dl.replaceChildren();const d=C.doctor;
 [["Name",d.name],["Qualification",d.qual],["Experience",d.exp],["Specialization",d.spec]].forEach(([a,v])=>dl.append(el("dt",t(a)),el("dd",v||"["+t("To be confirmed")+"]")));
 $("#dp-name").textContent=d.name||"["+t("To be confirmed")+"]";$("#dp-sub").textContent=[d.qual,d.exp,d.spec].filter(Boolean).join(" · ")||t("Qualifications and experience: ")+"["+t("To be confirmed")+"]";
 const ds=$("#dp-svc");ds.replaceChildren();C.svc.filter(x=>x.ok).forEach(x=>ds.append(el("span",nm(x))));if(!ds.children.length)ds.append(el("span","["+t("To be confirmed")+"]"));
 $("#dp-addr").textContent=C.address||"["+t("To be confirmed")+"]";
 const at=$("#atabs");at.replaceChildren();["Upcoming","Completed","Cancelled"].forEach((x,i)=>{const b=el("button",t(x),"chip");b.type="button";b.setAttribute("aria-pressed",String(i===0));b.onclick=()=>$$("#atabs .chip").forEach((c,j)=>c.setAttribute("aria-pressed",String(i===j)));at.append(b)});
 if(data)sum();renderHome();if(route()==="info")renderInfo();
}
function renderHome(){
 const d=C.doctor,tb="["+t("To be confirmed")+"]";
 $("#hd-name").textContent=d.name||tb;
 $("#hd-sub").textContent=[d.qual,d.exp,d.spec].filter(Boolean).join(" · ")||t("Qualifications and experience: ")+tb;
 const hc=$("#hc");hc.replaceChildren();
 [["Address",C.address],["Phone",C.phone?phoneTxt():""],["WhatsApp",waNum()?"+"+waNum()+(C.waConfirmed?"":" ["+t("to be confirmed")+"]"):""],["Email",C.email],["Hours",hoursTxt()],["Google rating",ratingTxt()]].filter(([k,v])=>k!=="Google rating"||v).forEach(([k,v])=>{const p=el("p");p.style.margin="0 0 6px";p.append(el("strong",t(k)+": "),v||tb);hc.append(p)});
 const on={call:!!telHref(),wa:!!waBase(),dir:!!(C.address&&safe(C.maps)),view:!!safe(C.mapsShort),mail:mailOk()};
 renderMap();renderRev();$("#callbk").hidden=!(telHref()&&!waBase());
 $$("#ha [data-act],#dp-acts [data-act]").forEach(b=>{const o=!on[b.dataset.act];b.classList.toggle("off",o);b.setAttribute("aria-disabled",String(o))});
}
function renderMap(){const m=$("#mapbox");if(m.querySelector("iframe"))return;m.replaceChildren();
 const c=el("div",null,"mapcard");c.append(el("span","📍","pin"),el("b",t("Find us on Google Maps")));
 const d=el("button","📍 "+t("Get Directions"),"btn");d.type="button";d.dataset.act="dir";d.id="getdir";const dirOk=!!(C.address&&safe(C.maps));if(!dirOk){d.classList.add("off");d.setAttribute("aria-disabled","true")}const n=el("p","","muted0");n.id="mapnote";const vOk=!!safe(C.mapsShort);const v=el("button","🗺️ "+t("View on Google Maps"),"btn o");v.type="button";v.dataset.act="view";v.id="viewmap";if(!vOk){v.classList.add("off");v.setAttribute("aria-disabled","true")}m.append(c,d,v);if(!dirOk){const sp=el("p",t("Setup needed: add the clinic's Google Maps link (maps) and address in config.js. Directions stay off until then."),"muted0");sp.id="mapsetup";sp.setAttribute("role","note");m.append(sp)}
 if(safeEmbed(C.mapEmbed)){const b=el("button",t("Show live map"),"btn o sm");b.type="button";b.dataset.act="map";b.style.marginTop="8px";n.textContent=t("Loads Google Maps. Google may collect visitor data.");m.append(b)}else n.textContent=t("Map is off until the clinic's address is confirmed.");
 m.append(n)}
function renderRev(){const r=ratingTxt();$("#rvtxt").textContent=r||t("No ratings or reviews are shown until the clinic adds its verified Google Maps profile link.");$("#rvnote").textContent=r?t("Open Google Maps to read the reviews."):""}
function sum(){const s=$("#sum");s.replaceChildren();const sv=C.svc.find(x=>x.id===data.tr);
 [["Full Name",data.name],["Mobile Number",data.phone],["Select Treatment",sv?nm(sv):""],["Preferred Date",data.date+", "+t(["Any time","Morning","Afternoon","Evening"][data.time])]].concat(data.msg?[["Additional Message (Optional)",data.msg]]:[]).forEach(([a,v])=>s.append(el("dt",t(a)),el("dd",v)));}
function renderInfo(){const kind=infoKind,b=$("#ib");b.replaceChildren();let ti="";
 if(kind==="hours"){ti="Opening Hours";const tb=el("table");C.hours.forEach(h=>{const r=el("tr");r.append(el("td",lang==="hi"?h.d[1]:h.d[0]),el("td",h.t?t(h.t):"["+t("To be confirmed")+"]"));tb.append(r)});b.append(tb,el("p",t("Weekly holiday")+": "+(C.holidays?dayName(C.holidays):"["+t("To be confirmed")+"]")));}
 else if(kind==="faq"){ti="FAQs";[["How do I book?","Use the request form, WhatsApp or call. The clinic confirms your slot."],["Is a request a confirmed booking?","No. A booking is confirmed only when the clinic replies."],["What about fees and timings?","Not published in this demo. Please ask the clinic."],["Can I cancel or reschedule?","Contact the clinic directly. Policy: to be confirmed."]].forEach(([a,c])=>{const d=el("details");d.append(el("summary",t(a)),el("p",t(c)));b.append(d)});}
 else{ti=kind==="privacy"?"Privacy (template)":"Terms (template)";b.append(el("p",t(kind==="privacy"?"Your form details are not sent to any server. They are put into a WhatsApp message on your device, and you choose whether to send it. Only your language choice is saved in your browser. If you tap Show live map, Google Maps loads and Google may collect data under its own policy. The clinic must review and complete this template.":"This site gives general information only. It is not medical advice or a diagnosis, and no outcome is guaranteed. A request is not a confirmed booking until the clinic confirms it. The clinic must review and complete this template.")));}
 if(kind==="privacy"||kind==="terms"){const a=el("a",t("Open full page"));a.href=kind+".html";b.append(a)}$("#it").textContent=t(ti);}
function setLang(){lang=lang==="en"?"hi":"en";try{localStorage.setItem("lang",lang)}catch(e){}render();}
$$(".langbtn").forEach(b=>b.onclick=setLang);$("#lg").onclick=setLang;
const ACT={
 wa(){const b=waBase();if(!b)return toast(t("WhatsApp is not set up yet. The clinic must add a verified number."));openUrl(b+"?text="+encodeURIComponent("Hello "+C.name+", I would like to ask about an appointment."))},
 call(){const h=telHref();if(!h)return toast(t("Phone number is not set up yet."));location.href=h},
 view(){const u=safe(C.mapsShort);if(!u)return toast(t("Google Maps link is not set up yet."));openUrl(u)},
 dir(){const u=C.address&&safe(C.maps);if(!u)return toast(t("Directions are off until the clinic's address and Maps link are confirmed."));openUrl(u)},
 mail(){if(!mailOk())return toast(t("Email is not set up yet."));location.href="mailto:"+C.email},
 map(){const u=safeEmbed(C.mapEmbed);if(!u)return toast(t("Map is off until the clinic's address is confirmed."));const f=el("iframe");f.src=u;f.title=t("Map showing the clinic location");f.loading="lazy";f.referrerPolicy="no-referrer";f.setAttribute("sandbox","allow-scripts allow-same-origin allow-popups");f.style.cssText="border:0;display:block;width:100%;height:clamp(220px,62vw,340px);max-width:100%;border-radius:14px;margin-bottom:8px";
   const note=$("#mapnote"),btn=$("#mapbox [data-act=map]");if(btn)btn.remove();note.textContent=t("Map not showing? Open it in Google Maps.");
   const onV=e=>{if(/google\./.test(e.blockedURI||"")){document.removeEventListener("securitypolicyviolation",onV);f.remove();note.textContent=t("The map cannot be embedded on this page. Open it in Google Maps.")}};document.addEventListener("securitypolicyviolation",onV);$("#mapbox").prepend(f)},
 rev(){const u=safe(C.reviews);if(!u)return toast(t("Reviews link is not set up yet."));openUrl(u)}};
document.addEventListener("click",e=>{const x=e.target.closest("[data-go],[data-back],[data-book],[data-info],[data-act],#clr");if(!x)return;
 if(x.id==="clr"){q="";cat="All";$("#q2").value="";$("#q").value="";return render()}
 if(x.dataset.back!==undefined)return go(PARENT[route()]||"home");
 if(x.dataset.go)return go(x.dataset.go);
 if(x.dataset.book){$("#f-tr").value=x.dataset.book;return go("book")}
 if(x.dataset.info)return go("info",x.dataset.info);
 if(ACT[x.dataset.act])ACT[x.dataset.act]()});
$("#q2").addEventListener("input",e=>{q=e.target.value.trim();render()});
const doSearch=()=>{q=$("#q").value.trim();cat="All";$("#q2").value=q;render();go("svc")};
$("#sf").onsubmit=e=>{e.preventDefault();doSearch()};$("#qgo").onclick=doSearch;
$("#q").addEventListener("keydown",e=>{if(e.key==="Enter"){e.preventDefault();doSearch()}});
$("#f-date").min=today();
const err=(k,m)=>{$("#e-"+k).textContent=m||"";const f=$("#f-"+k);if(f)f.setAttribute("aria-invalid",m?"true":"false")};
const submitBook=()=>{
 const v={name:$("#f-name").value.trim(),phone:$("#f-phone").value.replace(/[\s-]/g,""),tr:$("#f-tr").value,date:$("#f-date").value,time:$("#f-time").value,msg:$("#f-msg").value.trim()};
 const bad={name:!/^[\p{L}\p{M}][\p{L}\p{M} .'’-]{1,59}$/u.test(v.name)?t("Enter your name (2 to 60 characters)."):"",phone:/^(\+?91|0)?[6-9]\d{9}$/.test(v.phone)?"":t("Enter a valid 10-digit Indian mobile number."),tr:v.tr?"":t("Choose a treatment."),date:v.date&&v.date>=today()?"":t("Choose today or a future date."),ok:$("#f-ok").checked?"":t("Tick the consent box to continue.")};
 Object.keys(bad).forEach(k=>err(k,bad[k]));const f=Object.keys(bad).find(k=>bad[k]);if(f)return $("#f-"+f).focus();
 data=v;sum();$("#st").textContent="";step(2);$("#send").focus();};
$("#bsub").onclick=submitBook;
$("#bf").addEventListener("keydown",e=>{if(e.key==="Enter"&&e.target.tagName!=="TEXTAREA"&&e.target.tagName!=="BUTTON"){e.preventDefault();submitBook()}});
$("#bf").onsubmit=e=>{e.preventDefault();submitBook()};
$("#edit").onclick=()=>step(1);
function send(){const b=waBase();if(!b){$("#st").textContent=t("WhatsApp is not set up yet. The clinic must add a verified number.");return false}
 const sv=C.svc.find(s=>s.id===data.tr);
 const m=["Hello "+C.name+", I would like to request an appointment.","Name: "+data.name,"Phone: "+data.phone,"Treatment: "+(sv?sv.en:data.tr),"Preferred: "+data.date+", "+["Any time","Morning","Afternoon","Evening"][data.time],data.msg?"Message: "+data.msg:"","(Request only. Please confirm availability.)"].filter(Boolean).join("\n");
 waUrl=b+"?text="+encodeURIComponent(m);openUrl(waUrl);return true}
$("#send").onclick=()=>{const k=JSON.stringify(data);if(k===last.k&&Date.now()-last.a<6e4){$("#st").textContent=t("You already prepared this request a moment ago.");return}
 const b=$("#send");b.disabled=true;setTimeout(()=>b.disabled=false,4000);if(send()){last={k,a:Date.now()};step(3);$("#again").focus()}};
$("#again").onclick=()=>waUrl&&openUrl(waUrl);
$(".skip").addEventListener("click",e=>{e.preventDefault();$("#main").focus()});
render();show(route());
})();

/* Keep the field being typed in visible above the on-screen keyboard and the bottom navigation bar */
document.addEventListener("focusin",e=>{const f=e.target;if(f&&f.matches&&f.matches("input:not([type=checkbox]),textarea,select"))setTimeout(()=>{try{f.scrollIntoView({block:"center",behavior:"smooth"})}catch(x){}},350)});

/* CONFIG: edit here. Leave "" until verified. No secrets. */
const C={demo:true,name:"SN Dental Clinic",
 /* Leave "" until the CLINIC has verified each value. Nothing is invented; empty values show "To be confirmed" and disable the matching button. */
 address:"4R7M+7FX, Hoskote - Chintamani Rd, Pillagumpe, Chokkahalli, Karnataka 562114", // from the public Google Maps listing (screenshots 14 Oct 2026); clinic to confirm
 phone:"+917483582795", // listing shows 074835 82795; same number is on the roadside signboard. Not confirmed as WhatsApp
 whatsapp:"917483582795", // clinic phone number as supplied by the owner. NOT yet confirmed to be registered on WhatsApp (see waConfirmed). Digits only, country code first
 waConfirmed:false, // set true only after the clinic confirms this number receives WhatsApp messages; until then the site shows "to be confirmed" beside it
 email:"",       // official clinic email
 mapsShort:"https://maps.app.goo.gl/QhSLEoL1c7m7tq7p9?g_st=ac", // OFFICIAL clinic location link supplied by the owner; used by "View on Google Maps"
 maps:"https://www.google.com/maps/dir/?api=1&destination=4R7M%2B7FX+Hoskote%2C+Karnataka", // used by "Get Directions". The short link above cannot be used as a directions destination, so this uses the clinic plus code + town from the owner-supplied address. TO CONFIRM: open it once and check the pin matches the short link
 reviews:"https://www.google.com/maps/search/?api=1&query=SN+Dental+Clinic%2C+4R7M%2B7FX%2C+Hoskote+-+Chintamani+Rd%2C+Pillagumpe%2C+Chokkahalli%2C+Karnataka+562114", // opens the place card (Reviews tab); replace with the exact Share link if possible
 mapEmbed:"https://www.google.com/maps?q=4R7M%2B7FX+Hoskote%2C+Karnataka&z=17&output=embed", // loaded only after the visitor taps Show map
 rating:{score:5,count:3,asof:"2026-10-14"}, // Google Maps listing on that date; update or remove, never invent
 holidays:"Wednesday", // listing shows Wednesday closed; confirm it is the weekly holiday

doctor:{name:"",qual:"",exp:"",spec:""},
hours:[ // from the Google Maps listing (14 Oct 2026); festival days may differ; clinic to confirm
 ["Monday","सोमवार","9:00 AM – 7:00 PM"],
 ["Tuesday","मंगलवार","9:00 AM – 7:00 PM"],
 ["Wednesday","बुधवार","Closed"],
 ["Thursday","गुरुवार","9:00 AM – 7:00 PM"],
 ["Friday","शुक्रवार","9:00 AM – 7:00 PM"],
 ["Saturday","शनिवार","9:00 AM – 7:00 PM"],
 ["Sunday","रविवार","9:00 AM – 7:00 PM"]].map(d=>({d:[d[0],d[1]],t:d[2]})),
svc:[ // ok:1 only after the clinic confirms it offers the treatment; unconfirmed ones show a Sample tag in demo mode
{id:"checkup",c:"General",ok:0,en:"General Dentistry",de:"Check-ups and routine dental care",hi:"सामान्य दंत चिकित्सा",dh:"जांच और नियमित दंत देखभाल"},
{id:"cosmetic",c:"Cosmetic",ok:0,en:"Cosmetic Dentistry",de:"Options to improve your smile",hi:"कॉस्मेटिक दंत चिकित्सा",dh:"मुस्कान सुधारने के विकल्प"},
{id:"rct",c:"Advanced",ok:1,en:"Root Canal Treatment",de:"For deep tooth infection",hi:"रूट कैनाल उपचार",dh:"गहरे दांत संक्रमण के लिए"},
{id:"cleaning",c:"General",ok:0,en:"Teeth Cleaning",de:"Remove plaque and stains",hi:"दांतों की सफाई",dh:"प्लाक और दाग हटाना"},
{id:"filling",c:"General",ok:0,en:"Tooth Filling",de:"Repair cavities and damaged teeth",hi:"दांत की फिलिंग",dh:"कैविटी और टूटे दांत की मरम्मत"},
{id:"extraction",c:"General",ok:1,en:"Tooth Extraction",de:"Removal of a damaged tooth",hi:"दांत निकालना",dh:"क्षतिग्रस्त दांत हटाना"},
{id:"implants",c:"Advanced",ok:1,en:"Dental Implants",de:"An option for missing teeth",hi:"डेंटल इम्प्लांट",dh:"गायब दांतों का विकल्प"},
{id:"braces",c:"Cosmetic",ok:0,en:"Braces & Aligners",de:"Teeth alignment options",hi:"ब्रेसेस और एलाइनर",dh:"दांतों की स्थिति के विकल्प"},
{id:"whitening",c:"Cosmetic",ok:0,en:"Teeth Whitening",de:"Brighten your smile",hi:"दांतों की सफ़ेदी",dh:"मुस्कान निखारें"},
{id:"kids",c:"Kids",ok:0,en:"Children's Dentistry",de:"Dental care for children",hi:"बच्चों के दांतों की देखभाल",dh:"बच्चों के लिए दंत देखभाल"},
{id:"gum",c:"General",ok:1,en:"Gum Care",de:"Assessment of gum health",hi:"मसूड़ों की देखभाल",dh:"मसूड़ों की सेहत की जांच"}]};

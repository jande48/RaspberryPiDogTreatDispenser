(this["webpackJsonpreact-frontend"]=this["webpackJsonpreact-frontend"]||[]).push([[0],{104:function(e,t,c){var a={"./Tedi1.mp4":105,"./Tedi2.mp4":106,"./Tedi3.mp4":107};function n(e){var t=s(e);return c(t)}function s(e){if(!c.o(a,e)){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}return a[e]}n.keys=function(){return Object.keys(a)},n.resolve=s,e.exports=n,n.id=104},105:function(e,t,c){"use strict";c.r(t),t.default=c.p+"media/Tedi1.4a41e76b.mp4"},106:function(e,t,c){"use strict";c.r(t),t.default=c.p+"media/Tedi2.330869f4.mp4"},107:function(e,t,c){"use strict";c.r(t),t.default=c.p+"media/Tedi3.23ff7471.mp4"},109:function(e,t,c){"use strict";c.r(t);var a=c(1),n=c.n(a),s=c(16),r=c.n(s),i=(c(40),c(35),c(11)),d=c(8),o=(c.p,c.p+"media/tedi.d161a6e6.jpeg"),l=c(33),u=c.n(l),j=(c(42),c(43),c(14)),b=c.n(j),h=c(34),O=c.n(h),x=(c(78),c(2));var f=function(){var e=Object(a.useState)("waiting"),t=Object(d.a)(e,2),n=t[0],s=t[1],r=Object(a.useState)({}),l=Object(d.a)(r,2),j=l[0],h=l[1],f=Object(a.useState)(new Date),v=Object(d.a)(f,2),p=(v[0],v[1],Object(a.useState)("10:00")),m=Object(d.a)(p,2),T=m[0],g=m[1],y=Object(a.useState)("Today"),k=Object(d.a)(y,2),D=k[0],S=k[1],C=Object(a.useState)([]),P=Object(d.a)(C,2),w=P[0],E=P[1],N=Object(a.useState)([]),F=Object(d.a)(N,2),I=(F[0],F[1]);function M(e){var t=[];return e.keys().map((function(c,a){return t.push(e(c))})),t}var L=c(104),R=Object(a.useState)(M(L)),q=Object(d.a)(R,2),B=q[0];q[1],Object(a.useEffect)((function(){b.a.get("/getPickle").then((function(e){h(e.data),I(e.data.video.videoPaths),E(e.data.scheduledDispenseTreats)})).catch((function(e){return console.log(e)}))}),[B]);var G=function(e){b.a.post("/setPickle",e).then((function(e){h(e.data),I(e.data.video.videoPaths),E(e.data.scheduledDispenseTreats)})).catch((function(e){return console.log(e)}))},J=function(e){var t=Object(i.a)({},j);t.scheduledDispenseTreats.splice(e.target.name,1),G(t)};return console.log(B),Object(x.jsx)("div",{className:"App",children:Object(x.jsxs)("div",{class:"container",children:[Object(x.jsx)("img",{src:o,alt:"Tedi"}),"dispensing"==n?Object(x.jsx)("h2",{children:"... Dispensing Treat ... Recording Video .."}):Object(x.jsx)("button",{class:"big-treat-button",onClick:function(){s("dispensing"),b.a.post("/giveTreat",{id:"success"}).then((function(e){"success"==e.data.key?(s("dispensed"),console.log(M(L))):s("problem")})).catch((function(e){s("problem")}))},children:"Give Tedi a Treat!"}),Object(x.jsx)("h1",{class:"max-treats-per-day",children:"Max Treats Per Day"}),Object(x.jsxs)("div",{class:"max-treats-flexbox-container",children:[Object(x.jsx)("div",{class:"max-treats-box-1",children:Object(x.jsx)("button",{class:"big-treat-button",onClick:function(){var e=Object(i.a)({},j);e.maxNumOfTreatsPerDay>0&&(e.maxNumOfTreatsPerDay-=1,G(e))},children:"-"})}),Object(x.jsx)("div",{class:"max-treats-box-2",children:Object(x.jsx)("h1",{children:""+j.maxNumOfTreatsPerDay})}),Object(x.jsx)("div",{class:"max-treats-box-1",children:Object(x.jsx)("button",{class:"big-treat-button",onClick:function(){var e=Object(i.a)({},j);e.maxNumOfTreatsPerDay+=1,G(e)},children:"+"})})]}),Object(x.jsx)("h1",{class:"max-treats-per-day",children:"Schedule a Treat"}),Object(x.jsxs)("div",{class:"schedule-flexbox-container",children:[Object(x.jsx)("div",{class:"schedule-treat-box-1",children:Object(x.jsx)(O.a,{onChange:g,value:T,inverted:!0})}),Object(x.jsx)("div",{class:"schedule-treat-box-2",children:Object(x.jsx)(u.a,{placeholder:"Today",onChange:function(e){S(e.value)},options:[{key:"Today",text:"Today",value:"Today"},{key:"Tomorrow",text:"Tomorrow",value:"Tomorrow"},{key:"Everyday",text:"Everyday",value:"Everyday"}]})}),Object(x.jsx)("div",{class:"schedule-treat-box-3",children:Object(x.jsx)("button",{class:"schedule-button",onClick:function(){var e=Object(i.a)({},j),t=new Date;e.scheduledDispenseTreats.push({time:T,freq:D,scheduledDate:[parseInt(t.getFullYear()),parseInt(t.getMonth()+1),parseInt(t.getDate())]}),G(e)},children:"Schedule"})})]}),Object(x.jsx)("h1",{class:"scheduled-treats",children:"Scheduled Treats"}),w.map((function(e,t){return Object(x.jsx)("div",{children:Object(x.jsxs)("div",{class:"scheduled-flexbox-container",children:[Object(x.jsx)("div",{class:"scheduled-treat-box-1",children:Object(x.jsxs)("h2",{children:[e.freq," ",e.time]})}),Object(x.jsx)("div",{class:"scheduled-treat-box-2",children:Object(x.jsx)("button",{class:"remove-button",onClick:J,name:t,children:"Remove"})})]})})})),Object(x.jsx)("div",{children:Object(x.jsx)("button",{class:"remove-button",onClick:function(e){var t=Object(i.a)({},j);t.treatsGivenToday=0,G(t)},children:"Reset Treats Today"})})]})})},v=function(e){e&&e instanceof Function&&c.e(3).then(c.bind(null,111)).then((function(t){var c=t.getCLS,a=t.getFID,n=t.getFCP,s=t.getLCP,r=t.getTTFB;c(e),a(e),n(e),s(e),r(e)}))};r.a.render(Object(x.jsx)(n.a.StrictMode,{children:Object(x.jsx)(f,{})}),document.getElementById("root")),v()},40:function(e,t,c){},43:function(e,t,c){}},[[109,1,2]]]);
//# sourceMappingURL=main.74bdb551.chunk.js.map
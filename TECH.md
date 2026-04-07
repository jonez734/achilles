# Technical References

- https://suenawilliams.wordpress.com/2015/04/06/have-it-your-way/
- https://www.mcdonalds.com/us/en-us/about-our-food/nutrition-calculator.html
- https://menuandprice.com/which-restaurants-use-msg-in-their-food/
- https://www.naturalnews.com/kfc-chick-fil-a-burger-king-pizza-hut-msg-menu-items.html
- https://www.google.com/search?q=does+burger+king+have+msg%3F&oq=does+burger+&aqs=chrome.1.69i57j35i39j0i512l8.7152j0j7&sourceid=chrome&ie=UTF-8
- [It's a view, it's a table... no, it's a materialized view!](https://www.compose.com/articles/its-a-view-its-a-table-no-its-a-materialized-view/)
- https://www.google.com/search?q=materialized+view+allow+foreign+keys+postgresql&sxsrf=AOaemvKXiDjittSPv497xi3rPgqVwQIl4w%3A1634692176870&ei=UGxvYdyrNI-NwbkPutKp4Ag&ved=0ahUKEwjck5P05tfzAhWPRjABHTppCowQ4dUDCA4&uact=5&oq=materialized+view+allow+foreign+keys+postgresql&gs_lcp=Cgdnd3Mtd2l6EAMyBQghEKsCOgcIABBHELADOggIIRAWEB0QHjoFCCEQoAE6BAghEApKBAhBGABQp5cBWIqlAWDspQFoAXACeACAAXiIAf0HkgEDOS4ymAEAoAEByAEIwAEB&sclient=gws-wiz
- https://www.google.com/search?sxsrf=AOaemvI4eejhaAk5dp41MyB14zXfYY6QYA:1634690132974&q=Doritos+Cool+Ranch+Flavored+Tortilla+Chips&stick=H4sIAAAAAAAAAA3IMQrCMBQAUEQKOriIBwiOXdI4iHSteABxL2nySb79_T8kxd7H0RN4PH3j26z3Wz3pxpybJx13OmhjoqFwypehPoyu1U6mSbj1svBisy-flfkfEbgZhfXIshD4AH2yDFR0iZIScujH1ANhwIHgXdVXyThLUZ0IqbtlF9WN7EsyePWQPCORVV3EVL7V6gc7-3VplgAAAA&sa=X&ved=2ahUKEwiB68Wl39fzAhV_QTABHaJJDGAQxA16BAhJEAs&biw=1920&bih=978&dpr=1
- https://www.postgresqltutorial.com/postgresql-materialized-views/

# Technical TODO

- [ ] convert all tables to use engine.node
    * [ ] fooditem
    * [ ] attachment
    * [ ] merchant
    * [x] retailer
    * [x] symptom
    * [x] vendor
    * [ ] lab
    * [ ] test
    * [ ] ingredient

- [ ] allow multiple ingredients, upc photos in case vendor changes graphics @since 20220106

- examples:
    * https://www.jimmydean.com/products/simple-scrambles/meat-lovers-simple-scrambles/

- [ ] fooditems can be in sig(s) for organizing.

- [ ] make a way to handle a corp like "GFS" which distributes seasonings to restaurants, etc, and a website stating which of their products use msg (I could find none)
    * https://en.wikipedia.org/wiki/Gordon_Food_Service

- contributors
  * scott (us army veteran) for the name 'fooditem' for one of the database tables
  * my dad for helping me w chemistry basics and reading my webpage
  * dr. aaron for letting me know that he recommends that all of his patients stay away from msg.

- [ ] detect upc code on a given image.
    * libzbar only installs for python 2.7, it has no accomodation for 3
      when building the extension.
    * zbarlight looked promising and in fact claims to work with python3,
      however it depends on libzbar.so.0
    * https://www.geeksforgeeks.org/how-to-make-a-barcode-reader-in-python/
    * https://pypi.org/project/python-barcode/
    * https://pypi.org/project/pyzbar-x/#files
    * https://sourceforge.net/projects/zbar/
    * https://pypi.org/project/pyzbar/
    * https://techtutorialsx.com/2020/01/01/python-pyzbar-detecting-and-decoding-barcode/
    * https://stackoverflow.com/questions/46610689/how-to-import-cv2-in-python3
    * https://pypi.org/project/python-barcode/
    * https://www.geeksforgeeks.org/how-to-make-a-barcode-reader-in-python/ python2?
    * https://www.upcindex.com/api

- [ ] drop down arrow for sections (@ty pscug)
- [ ] wordy, duplicate info (@ty pscug)
- [38 HTML <details> & <summary> with CSS](https://freefrontend.com/html-details-summary-css/)

- zbar is inadequate.. it only handles UPC that are face-on, pure white background. no angles or extra colors. (@since 20220106)

- https://iq.opengenus.org/convert-jpg-to-png-in-python/
- https://omz-software.com/pythonista/docs/ios/Image.html
- https://installati.one/fedora/34/zbar/
- https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/checkbutton.html
- https://www.geeksforgeeks.org/python-tkinter-text-widget/
- https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/fonts.html
- https://stackoverflow.com/questions/15672552/tkinter-listbox-getactive-method

# Grant Proposal Notes

- @since 20221216 added
- @see https://chat.openai.com/chat :

It is important to carefully consider the potential risks and benefits of any research proposal before submitting it for funding. Here are some considerations to keep in mind when proposing a grant to study the effects of monosodium glutamate (MSG) and other flavor enhancers:

    Research question: Clearly define the research question you are trying to address. What specifically do you hope to learn about the effects of MSG and other flavor enhancers?

    Background and significance: Provide a review of the existing literature on MSG and other flavor enhancers, highlighting any gaps or controversies that your research aims to address. Explain the potential implications of your research for public health or industry.

    Methodology: Outline the specific methods you will use to study the effects of MSG and other flavor enhancers. This should include a description of the study design, sample size, and inclusion/exclusion criteria.

    Ethical considerations: Discuss any potential ethical concerns that may arise in your research, and describe how you will address them. This may include obtaining informed consent from participants, protecting their privacy, and minimizing any potential harm.

    Budget and timeline: Include a detailed budget outlining the resources needed to complete the research, as well as a timeline for completing the various stages of the study.

By considering these elements in your grant proposal, you can increase the likelihood that it will be well-received by potential funding sources.

- @since 20221216
- @see "explain to a congressman the harms of msg"

# MSG Scientific Background

Monosodium glutamate (MSG) is a flavor enhancer that is commonly used in
processed foods, such as snack foods, soups, frozen dinners and some quick
service restaurants.  Some people have reported adverse reactions after
consuming foods containing MSG, including headache, flushing, and difficulty
breathing.  However, the evidence for a link between MSG and these reactions
is not clear and more research is needed to confirm whether MSG is a cause
of these symptoms.

It is also worth noting that MSG is generally recognized as safe by
regulatory agencies around the world, including the US Food and Drug
Administration (FDA).  The FDA considers MSG to be a food ingredient that is
"generally recognized as safe" (GRAS) when consumed at normal levels.

While the potential risks of MSG remain somewhat controversial, it is
important for consumers to be aware of the potential for adverse reactions
and to make informed decisions about their dietary choices.  Some
individuals may choose to avoid foods that contain MSG, while others may be
comfortable consuming foods that contain the ingredient.  Ultimately, the
decision about whether to consume MSG or other food additives is a personal
one that should be based on individual preferences and considerations.

---

Monosodium glutamate (MSG) is a flavor enhancer that is commonly used in
food.  It is a salt of the amino acid glutamate, which is found naturally in
many foods, including meat, dairy products, and vegetables.

When MSG comes into contact with a cell, it can interact with receptors on
the surface of the cell membrane.  These receptors, known as glutamate
receptors, are found on cells throughout the body and are involved in a
variety of functions, including learning, memory, and the transmission of
signals between nerve cells.

When MSG binds to these receptors, it can activate them and cause the cell
to respond in a specific way.  For example, it may stimulate the release of
neurotransmitters, which are chemicals that transmit signals between nerve
cells.

Here is a simplified illustration of the process of MSG coming into contact with a cell:

    MSG is consumed and enters the body through the digestive system.

    It is absorbed into the bloodstream and transported to various parts of the body.

    MSG comes into contact with a cell, such as a nerve cell or a muscle cell.

    MSG binds to receptors on the surface of the cell membrane.

    The binding of MSG to the receptors activates the receptors and causes the cell to respond in a specific way.

    The response of the cell may include the release of neurotransmitters or other chemicals, or the activation of specific pathways within the cell.

# Ingredient vs Additive

this is from 2023-07-17:

User
is there a difference between an ingredient and an additive?
ChatGPT

Yes, there is a difference between an ingredient and an additive.

An ingredient is a fundamental component or substance used in the preparation of a product or dish. It contributes to the essential character, flavor, or nutritional value of the final product. In cooking or food manufacturing, ingredients are typically natural or basic items such as fruits, vegetables, grains, meats, spices, oils, etc. For example, in a recipe for a cake, ingredients would include flour, sugar, eggs, butter, and so on.

On the other hand, an additive is a substance that is added to a product during processing or manufacturing. Additives are not necessarily natural or basic components like ingredients. They are used for various purposes, such as preserving the product, enhancing its flavor, improving its texture, or extending its shelf life. Additives can be synthetic or derived from natural sources. Examples of additives include preservatives, food coloring, flavor enhancers, stabilizers, emulsifiers, and sweeteners.

While all additives are technically ingredients since they are added to a product, not all ingredients are additives. Ingredients are more commonly associated with the primary components of a recipe or formulation, whereas additives are additional substances incorporated for specific purposes beyond the core ingredients.

It's important to note that additives undergo rigorous safety assessments and regulatory approval processes before they are permitted for use in food or other products. They are subject to specific regulations and guidelines to ensure consumer safety and product quality.
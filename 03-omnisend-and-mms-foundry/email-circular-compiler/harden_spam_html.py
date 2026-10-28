import os

table_only_html = """<table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" align="center" style="width: 100%; table-layout: fixed; margin: 0 auto; background-color: #FAF8F5; font-family: 'Garamond', 'Georgia', 'Times New Roman', serif;">
  <tr>
    <td align="center" style="padding: 18px 0; text-align: center;">
      <table role="presentation" class="tcc-outer-frame" cellspacing="0" cellpadding="0" border="0" width="640" align="center" style="width: 640px; max-width: 96%; table-layout: fixed; margin: 0 auto; background-color: #FFFFFF; border-left: 1.5px solid #B7A486; border-right: 1.5px solid #B7A486; border-top: 4px solid #701D32; border-bottom: 4px solid #701D32; box-sizing: border-box; text-align: left;">
        <tr>
          <td class="tcc-section-pad" align="center" style="padding: 22px 3.5% 12px 3.5%; background-color: #FFFFFF; box-sizing: border-box; text-align: center;">
            <a href="https://thechapmancollection.com/" target="_blank" style="text-decoration: none;">
              <img src="https://thechapmancollection.com/wp-content/uploads/2026/10/tcc-oct23-crest.png" alt="The Chapman Collection" width="80" style="display: block; margin: 0 auto 10px auto; width: 80px; max-width: 80px; height: auto; border: 0;">
            </a>
            <h1 style="margin: 0 0 8px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 24px; letter-spacing: 2.2px; text-transform: uppercase; color: #1F1D1C; font-weight: normal; line-height: 1.25; text-align: center;">
              The Chapman Collection
            </h1>
            <p class="tcc-subnav" style="margin: 0; padding: 0 0 14px 0; border-bottom: 1px solid #D5C7A3; font-family: 'Garamond', 'Georgia', serif; font-size: 8.5px; letter-spacing: 0.2px; text-transform: uppercase; color: #8C6D46; font-weight: bold; line-height: 1.6; text-align: center;">
              <a href="https://thechapmancollection.com/product-category/carpets/" target="_blank" style="color: #8C6D46; text-decoration: none; white-space: nowrap;">Persian Carpets</a>
              <span style="color: #B7A486; padding: 0 2px;">|</span>
              <a href="https://thechapmancollection.com/product-category/furniture/" target="_blank" style="color: #8C6D46; text-decoration: none; white-space: nowrap;">Fine Furniture</a>
              <span style="color: #B7A486; padding: 0 2px;">|</span>
              <a href="https://thechapmancollection.com/product-category/artwork-tapestries/" target="_blank" style="color: #8C6D46; text-decoration: none; white-space: nowrap;">Artworks</a>
              <span style="color: #B7A486; padding: 0 2px;">|</span>
              <a href="https://thechapmancollection.com/product-category/accessories/" target="_blank" style="color: #8C6D46; text-decoration: none; white-space: nowrap;">Accessories</a>
            </p>
          </td>
        </tr>
        <tr>
          <td class="tcc-section-pad" align="center" style="padding: 4px 3.5% 10px 3.5%; background-color: #FFFFFF; box-sizing: border-box; text-align: center;">
            <h2 style="margin: 0; font-family: 'Garamond', 'Georgia', serif; font-size: 26px; line-height: 1.25; color: #701D32; font-weight: normal; font-style: italic; text-align: center;">A little overdue, and so much to share</h2>
          </td>
        </tr>
        <tr>
          <td class="tcc-section-pad" style="padding: 2px 3.5% 8px 3.5%; background-color: #FFFFFF; box-sizing: border-box;">
            <p style="margin: 0 0 4px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 17.5px; line-height: 1.65; color: #24211F; text-align: left;">It has been a while since you last heard from us! We’ve been busy sourcing wonderful new arrivals for the showroom and helping clients furnish their homes, and we’re delighted to share a little preview of our latest finds.</p>
          </td>
        </tr>
        <tr>
          <td class="tcc-section-pad" style="padding: 6px 3.5% 12px 3.5%; background-color: #FFFFFF; box-sizing: border-box;">
            <h3 style="margin: 4px 0 10px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 22px; color: #701D32; font-weight: normal; letter-spacing: 0.5px; border-bottom: 1px solid #D5C7A3; padding-bottom: 5px; text-align: left;">
              Persian Carpets
            </h3>
            <p style="margin: 0 0 14px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 17.5px; line-height: 1.65; color: #24211F; text-align: left;">We’ve just received 45 Persian silk and silk-and-wool carpets via Dubai, pairing intricate Qum designs with fresh, contemporary color palettes. From bedside rugs and runners to generous living and dining room sizes, all are currently offered at special sale prices.</p>
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%; table-layout: fixed;">
              <tr>
                <td class="tcc-col" width="48.5%" valign="top" style="width: 48.5%; border: 1px solid #C8B68E; background-color: #FFFFFF; padding: 9px; box-sizing: border-box; text-align: left;">
                  <a href="https://thechapmancollection.com/product/new-persian-hand-finished-silk-qum-carpet-blue-turquoise-vintage-design/" target="_blank" style="text-decoration: none;">
                    <img src="https://thechapmancollection.com/wp-content/uploads/2026/10/tcc-oct23-carpet-1-medallion.jpg" alt="Persian Medallion Carpet" style="width: 100%; max-width: 255px; height: auto; display: block; margin: 0 auto; border: 0;">
                  </a>
                  <p style="margin: 10px 0 2px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 15px; line-height: 1.5; color: #2C2825; text-align: left;">Blending classic and contemporary style, this carpet pairs an elaborate central medallion with softly shaded blues, cream and warm gold for a living or dining room.</p>
                </td>
                <td class="tcc-spacer" width="3%" style="width: 3%;"></td>
                <td class="tcc-col" width="48.5%" valign="top" style="width: 48.5%; border: 1px solid #C8B68E; background-color: #FFFFFF; padding: 9px; box-sizing: border-box; text-align: left;">
                  <a href="https://thechapmancollection.com/product/new-persian-hand-finished-silk-qum-carpet-teal-all-over-floral-design/" target="_blank" style="text-decoration: none;">
                    <img src="https://thechapmancollection.com/wp-content/uploads/2026/10/tcc-oct23-carpet-2-teal-silk.jpg" alt="Pure Silk Teal Persian Carpet" style="width: 100%; max-width: 255px; height: auto; display: block; margin: 0 auto; border: 0;">
                  </a>
                  <p style="margin: 10px 0 2px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 15px; line-height: 1.5; color: #2C2825; text-align: left;">For a richer splash of color, this pure silk carpet features a delicate all-over floral design on a striking teal ground for an entrance, bedroom, office or coffee table.</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td class="tcc-section-pad" style="padding: 6px 3.5% 12px 3.5%; background-color: #FFFFFF; box-sizing: border-box;">
            <h3 style="margin: 4px 0 10px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 22px; color: #701D32; font-weight: normal; letter-spacing: 0.5px; border-bottom: 1px solid #D5C7A3; padding-bottom: 5px; text-align: left;">
              Antique Furniture
            </h3>
            <p style="margin: 0 0 14px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 17.5px; line-height: 1.65; color: #24211F; text-align: left;">We’ve also welcomed some beautiful antique furniture, including these two elegant French pieces.</p>
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%; table-layout: fixed;">
              <tr>
                <td class="tcc-col" width="48.5%" valign="top" style="width: 48.5%; border: 1px solid #C8B68E; background-color: #FFFFFF; padding: 9px; box-sizing: border-box; text-align: left;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%;">
                    <tr>
                      <td height="210" valign="middle" align="center" style="height: 210px; text-align: center;">
                        <a href="https://thechapmancollection.com/product/french-louis-xv-style-writing-desk-with-bronze-mounts/" target="_blank" style="text-decoration: none;">
                          <img src="https://thechapmancollection.com/wp-content/uploads/2026/10/tcc-oct23-furn-1-french-desk.jpg" alt="French Desk with Bronze Mounts" style="width: 100%; max-width: 260px; height: auto; display: block; margin: 0 auto; border: 0;">
                        </a>
                      </td>
                    </tr>
                  </table>
                  <p style="margin: 10px 0 2px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 15px; line-height: 1.5; color: #2C2825; text-align: left;">This handsome French desk combines rich wood tones, graceful curves, decorative bronze mounts and three practical drawers for a study or home office.</p>
                </td>
                <td class="tcc-spacer" width="3%" style="width: 3%;"></td>
                <td class="tcc-col" width="48.5%" valign="top" style="width: 48.5%; border: 1px solid #C8B68E; background-color: #FFFFFF; padding: 9px; box-sizing: border-box; text-align: left;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%;">
                    <tr>
                      <td height="210" valign="middle" align="center" style="height: 210px; text-align: center;">
                        <a href="https://thechapmancollection.com/product/antique-french-louis-xv-style-marquetry-commode-with-rouge-marble-top/" target="_blank" style="text-decoration: none;">
                          <img src="https://thechapmancollection.com/wp-content/uploads/2026/10/tcc-oct23-furn-2-french-commode.jpg" alt="French Marble-Top Commode" style="width: 100%; max-width: 225px; height: auto; display: block; margin: 0 auto; border: 0;">
                        </a>
                      </td>
                    </tr>
                  </table>
                  <p style="margin: 10px 0 2px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 15px; line-height: 1.5; color: #2C2825; text-align: left;">Topped with richly veined red marble, this French commode pairs patterned wood veneers and ornate bronze mounts to bring warmth to any room or entrance.</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td class="tcc-section-pad" style="padding: 6px 3.5% 12px 3.5%; background-color: #FFFFFF; box-sizing: border-box;">
            <h3 style="margin: 4px 0 10px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 22px; color: #701D32; font-weight: normal; letter-spacing: 0.5px; border-bottom: 1px solid #D5C7A3; padding-bottom: 5px; text-align: left;">
              Artwork
            </h3>
            <p style="margin: 0 0 14px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 17.5px; line-height: 1.65; color: #24211F; text-align: left;">From classical scenes to more contemporary works, here are two of my favorite pieces currently in the showroom.</p>
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%; table-layout: fixed;">
              <tr>
                <td class="tcc-col" width="48.5%" valign="top" style="width: 48.5%; border: 1px solid #C8B68E; background-color: #FFFFFF; padding: 9px; box-sizing: border-box; text-align: left;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%;">
                    <tr>
                      <td height="230" valign="middle" align="center" style="height: 230px; text-align: center;">
                        <a href="https://thechapmancollection.com/product/italian-oil-painting-depicting-the-venetian-grand-canal/" target="_blank" style="text-decoration: none;">
                          <img src="https://thechapmancollection.com/wp-content/uploads/2026/10/tcc-oct23-art-1-italian-royal-canal-straight.jpg" alt="Italian Oil Painting of the Grand Canal in Venice" style="width: 100%; max-width: 265px; height: auto; display: block; margin: 0 auto; border: 0;">
                        </a>
                      </td>
                    </tr>
                  </table>
                  <p style="margin: 10px 0 2px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 15px; line-height: 1.5; color: #2C2825; text-align: left;">Bring the romance of Venice into your home with this stunning Italian oil painting, capturing the beauty and bustle of the Grand Canal. Gondolas, magnificent architecture and luminous blue skies create a captivating scene, beautifully complemented by a classic frame. Newly painted and generously sized at 45″ high x 57″ wide.</p>
                </td>
                <td class="tcc-spacer" width="3%" style="width: 3%;"></td>
                <td class="tcc-col" width="48.5%" valign="top" style="width: 48.5%; border: 1px solid #C8B68E; background-color: #FFFFFF; padding: 9px; box-sizing: border-box; text-align: left;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%;">
                    <tr>
                      <td height="230" valign="middle" align="center" style="height: 230px; text-align: center;">
                        <a href="https://thechapmancollection.com/product/henri-matisse-blue-nude-iii-original-color-plate-in-custom-frame/" target="_blank" style="text-decoration: none;">
                          <img src="https://thechapmancollection.com/wp-content/uploads/2026/10/tcc-oct23-art-2-matisse-litho.jpg" alt="Framed Lithograph of Henri Matisse Blue Nude III" style="width: 100%; max-width: 205px; height: auto; display: block; margin: 0 auto; border: 0;">
                        </a>
                      </td>
                    </tr>
                  </table>
                  <p style="margin: 10px 0 2px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 15px; line-height: 1.5; color: #2C2825; text-align: left;">For a more modern look, this framed original color plate lithograph rendition of Henri Matisse’s Blue Nude III pairs vivid blue with the graceful, simplified curves of the seated figure inside a striking black surround and silver-toned frame.</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td class="tcc-section-pad" style="padding: 6px 3.5% 12px 3.5%; background-color: #FFFFFF; box-sizing: border-box;">
            <h3 style="margin: 4px 0 10px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 22px; color: #701D32; font-weight: normal; letter-spacing: 0.5px; border-bottom: 1px solid #D5C7A3; padding-bottom: 5px; text-align: left;">
              Decorative Accessories
            </h3>
            <p style="margin: 0 0 14px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 17.5px; line-height: 1.65; color: #24211F; text-align: left;">Our latest arrivals also include wonderful decorative pieces, from a stately grandfather clock to finely detailed porcelain urns and vases.</p>
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%; table-layout: fixed;">
              <tr>
                <td class="tcc-col-3" width="32%" valign="top" style="width: 32%; border: 1px solid #C8B68E; background-color: #FFFFFF; padding: 7px; box-sizing: border-box; text-align: left; word-break: break-word; overflow-wrap: break-word;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%;">
                    <tr>
                      <td height="185" valign="middle" align="center" style="height: 185px; text-align: center;">
                        <a href="https://thechapmancollection.com/product/traditional-american-grandfather-clock/" target="_blank" style="text-decoration: none;">
                          <img src="https://thechapmancollection.com/wp-content/uploads/2026/10/tcc-oct23-acc-1-grandfather-clock.jpg" alt="American Grandfather Clock" style="width: 100%; max-width: 68px; height: auto; display: block; margin: 0 auto; border: 0;">
                        </a>
                      </td>
                    </tr>
                  </table>
                  <p style="margin: 10px 0 2px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 14px; line-height: 1.48; color: #2C2825; text-align: left;">Handsome American grandfather clock with a richly toned wooden case, swan-neck pediment and ornate dial for an entrance hall or living room.</p>
                </td>
                <td class="tcc-spacer" width="2%" style="width: 2%;"></td>
                <td class="tcc-col-3" width="32%" valign="top" style="width: 32%; border: 1px solid #C8B68E; background-color: #FFFFFF; padding: 7px; box-sizing: border-box; text-align: left; word-break: break-word; overflow-wrap: break-word;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%;">
                    <tr>
                      <td height="185" valign="middle" align="center" style="height: 185px; text-align: center;">
                        <a href="https://thechapmancollection.com/product/pair-of-royal-vienna-style-hand-painted-porcelain-urns/" target="_blank" style="text-decoration: none;">
                          <img src="https://thechapmancollection.com/wp-content/uploads/2026/10/tcc-oct23-acc-2-vienna-urns.jpg" alt="Royal Vienna-Style Porcelain Urns" style="width: 100%; max-width: 155px; height: auto; display: block; margin: 0 auto; border: 0;">
                        </a>
                      </td>
                    </tr>
                  </table>
                  <p style="margin: 10px 0 2px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 14px; line-height: 1.48; color: #2C2825; text-align: left;">Hand-painted Royal Vienna-style porcelain urns combining classical figure scenes with rich burgundy, turquoise accents and gilding for a mantel or console.</p>
                </td>
                <td class="tcc-spacer" width="2%" style="width: 2%;"></td>
                <td class="tcc-col-3" width="32%" valign="top" style="width: 32%; border: 1px solid #C8B68E; background-color: #FFFFFF; padding: 7px; box-sizing: border-box; text-align: left; word-break: break-word; overflow-wrap: break-word;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%;">
                    <tr>
                      <td height="185" valign="middle" align="center" style="height: 185px; text-align: center;">
                        <a href="https://thechapmancollection.com/product/pair-of-chinese-polychrome-dragon-vases/" target="_blank" style="text-decoration: none;">
                          <img src="https://thechapmancollection.com/wp-content/uploads/2026/10/tcc-oct23-acc-3-dragon-vases.jpg" alt="Pair of Chinese Vases with Raised Dragons" style="width: 100%; max-width: 155px; height: auto; display: block; margin: 0 auto; border: 0;">
                        </a>
                      </td>
                    </tr>
                  </table>
                  <p style="margin: 10px 0 2px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 14px; line-height: 1.48; color: #2C2825; text-align: left;">Distinctive Chinese vases featuring intricate raised dragons, scrolling foliage and rich red, turquoise and gold tones to bring color and texture to a room.</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td class="tcc-section-pad" style="padding: 6px 3.5% 18px 3.5%; background-color: #FFFFFF; box-sizing: border-box;">
            <h3 style="margin: 4px 0 12px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 22px; color: #701D32; font-weight: normal; letter-spacing: 0.5px; border-bottom: 1px solid #D5C7A3; padding-bottom: 5px; text-align: left;">
              A Little News to Celebrate
            </h3>
            <a href="https://thechapmancollection.com/about-us/" target="_blank" style="text-decoration: none;">
              <img src="https://thechapmancollection.com/wp-content/uploads/2026/10/tcc-oct23-award-ranch-and-coast-2026.jpg" alt="Ranch and Coast Best Antique Store 2026" style="width: 100%; max-width: 100%; height: auto; display: block; margin: 0 auto 14px auto; border: 0;">
            </a>
            <p style="margin: 0 0 10px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 17.5px; line-height: 1.65; color: #24211F; text-align: left;">And finally, please excuse a little bragging! We’re delighted to share that The Chapman Collection has once again been recognized by Ranch &amp; Coast magazine as Best Antique Store for 2026, and we’re so grateful to our wonderful clients for your continued support.</p>
            <p style="margin: 0 0 16px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 17.5px; line-height: 1.65; color: #24211F; text-align: left;">We are open seven days a week in Rancho Santa Fe (Sundays by appointment), or simply let us know what you’re looking for and we would be delighted to send you a selection of pieces for your home or office.</p>
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%; margin: 14px 0 18px 0;">
              <tr>
                <td align="center" style="text-align: center;">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin: 0 auto;">
                    <tr>
                      <td bgcolor="#701D32" align="center" style="background-color: #701D32; border: 1px solid #C5A059; border-radius: 2px; text-align: center;">
                        <a href="https://thechapmancollection.com/" target="_blank" style="background-color: #701D32; color: #FFFFFF; text-decoration: none; font-family: 'Garamond', 'Georgia', 'Times New Roman', serif; font-size: 18px; font-weight: normal; letter-spacing: 0.2px; padding: 12px 28px; display: inline-block; border-radius: 2px; box-sizing: border-box; text-align: center;"><span style="color: #FFFFFF;">Browse Our Inventory Here</span></a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
            <p style="margin: 0 0 6px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 17.5px; line-height: 1.65; color: #24211F; font-weight: normal; text-align: left;">Hope to see you soon!</p>
            <p style="margin: 0 0 16px 0; font-family: 'Garamond', 'Georgia', serif; font-size: 17.5px; line-height: 1.65; color: #24211F; font-weight: normal; text-align: left;">Warmly,<br>Melissa Chapman</p>
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="width: 100%; background-color: #FFFFFF; border-top: 1px solid #EAE4D8; padding-top: 14px;">
              <tr>
                <td width="52" valign="middle" align="center" style="width: 52px; padding-right: 10px; border-right: 1px solid #D5C7A3;">
                  <img src="https://thechapmancollection.com/wp-content/uploads/2026/10/tcc-oct23-crest.png" alt="The Chapman Collection" width="44" style="width: 44px; max-width: 44px; height: auto; display: block; border: 0;">
                </td>
                <td valign="middle" style="padding-left: 10px; font-family: 'Garamond', 'Georgia', serif; color: #1F1D1C; text-align: left;">
                  <p style="margin: 0 0 3px 0; font-size: 13px; font-weight: bold; letter-spacing: 0.6px; text-transform: uppercase; color: #8C6D46; line-height: 1.35;">
                    THE CHAPMAN COLLECTION
                  </p>
                  <p style="margin: 0 0 3px 0; font-size: 12px; line-height: 1.45; color: #3D3935;">
                    <a href="https://thechapmancollection.com/call/" target="_blank" style="color: #1F1D1C; text-decoration: none; font-weight: bold;">(858) 349-2638</a>
                    <span style="color: #B7A486; padding: 0 4px;">|</span>
                    <a href="https://www.google.com/maps/search/?api=1&amp;query=The+Chapman+Collection+6014+La+Granada+Rancho+Santa+Fe+CA+92067" target="_blank" style="color: #3D3935; text-decoration: none;">6014 La Granada, Rancho Santa Fe, CA 92067</a>
                  </p>
                  <p style="margin: 0; font-size: 10.5px; letter-spacing: 0.5px; color: #701D32; font-weight: bold; line-height: 1.5;">
                    <a href="https://thechapmancollection.com/" target="_blank" style="color: #701D32; text-decoration: none;">WEBSITE</a>
                    <span style="color: #B7A486; padding: 0 4px;">|</span>
                    <a href="https://www.instagram.com/thechapmancollection/" target="_blank" style="color: #701D32; text-decoration: none;">INSTAGRAM</a>
                    <span style="color: #B7A486; padding: 0 4px;">|</span>
                    <a href="https://www.facebook.com/TheChapmanCollection" target="_blank" style="color: #701D32; text-decoration: none;">FACEBOOK</a>
                    <span style="color: #B7A486; padding: 0 4px;">|</span>
                    <a href="https://www.youtube.com/channel/UC7UeuQIpG2-o8ULUhhWDHQA" target="_blank" style="color: #701D32; text-decoration: none;">YOUTUBE</a>
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
"""

full_import_head = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>A little overdue, new arrivals from The Chapman Collection</title>
<style type="text/css">
  body, table, td, p, a, h1, h2, h3 {
    -webkit-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
  }
  table {
    border-collapse: collapse;
    mso-table-lspace: 0pt;
    mso-table-rspace: 0pt;
  }
  img {
    border: 0;
    height: auto;
    line-height: 100%;
    outline: none;
    text-decoration: none;
    max-width: 100%;
  }
  @media only screen and (max-width: 480px) {
    .tcc-outer-frame {
      width: 94% !important;
      max-width: 94% !important;
    }
    .tcc-section-pad {
      padding-left: 4.5% !important;
      padding-right: 4.5% !important;
    }
    .tcc-col, .tcc-col-3 {
      display: block !important;
      width: 100% !important;
      max-width: 100% !important;
      margin: 0 auto 14px auto !important;
      box-sizing: border-box !important;
    }
    .tcc-spacer {
      display: none !important;
      width: 0 !important;
      height: 0 !important;
    }
  }
</style>
</head>
<body style="margin:0;padding:0;background-color:#FAF8F5;">
"""

base_dir = r"C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\drafts-for-chapman-marshall-college-approval"
with open(os.path.join(base_dir, "2026-10-23-Omnisend_Custom_HTML_Block_Table_Only.html"), "w", encoding="utf-8") as f:
    f.write(table_only_html)

with open(os.path.join(base_dir, "2026-10-23-Omnisend_Saved_Template_Full_Import.html"), "w", encoding="utf-8") as f:
    f.write(full_import_head + table_only_html + "</body>\n</html>\n")

print("Wrote spam-hardened HTML to both files!")

#!/usr/bin/python
import sys
from bs4 import BeautifulSoup

html = """
 <table class="desktop">
  <thead>
    <tr class="lower">
      <th class="name">State</th>
      <th class="sep">Electoral votes</th>
      <th class="lower">College-educated white</th>
      <th class="lower">Non-college-educated white</th>
      <th class="lower">Black</th>
      <th class="lower">Hispanic/Latino</th>
      <th class="sep lower">Asian/Other</th>
      <th class="lower">Dems</th>
      <th class="lower">Reps</th>
    </tr>
  </thead>
  <tbody>
    <tr data-state="USA" class="state USA">
      <td class="name">U.S.</td>
      <td class="ev sep">
        <div>538
        </div>
      </td>
      <td data-category="CEW" class="pct share">30.0%</td>
      <td data-category="NCEW" class="pct share">36.6%</td>
      <td data-category="Black" class="pct share">12.5%</td>
      <td data-category="Latino" class="pct share">13.8%</td>
      <td data-category="A/O" class="pct share sep">7.0%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #82c4e4">45.9%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f88772">52.4%</div>
      </td>
    </tr>
    <tr data-state="Alabama" class="state Alabama">
      <td class="name">Ala.</td>
      <td class="ev sep">
        <div>9
        </div>
      </td>
      <td data-category="CEW" class="pct share">25.8%</td>
      <td data-category="NCEW" class="pct share">41.1%</td>
      <td data-category="Black" class="pct share">27.4%</td>
      <td data-category="Latino" class="pct share">2.8%</td>
      <td data-category="A/O" class="pct share sep">2.9%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #9bcee6">35.5%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #fa7158">63.4%</div>
      </td>
    </tr>
    <tr data-state="Alaska" class="state Alaska">
      <td class="name">Alaska</td>
      <td class="ev sep">
        <div>3
        </div>
      </td>
      <td data-category="CEW" class="pct share">25.0%</td>
      <td data-category="NCEW" class="pct share">45.4%</td>
      <td data-category="Black" class="pct share">2.6%</td>
      <td data-category="Latino" class="pct share">10.1%</td>
      <td data-category="A/O" class="pct share sep">16.9%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #85c5e4">44.7%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f88975">51.1%</div>
      </td>
    </tr>
    <tr data-state="Arizona" class="state Arizona">
      <td class="name">Ariz.</td>
      <td class="ev sep">
        <div>11
        </div>
      </td>
      <td data-category="CEW" class="pct share">28.1%</td>
      <td data-category="NCEW" class="pct share">39.3%</td>
      <td data-category="Black" class="pct share">3.5%</td>
      <td data-category="Latino" class="pct share">23.5%</td>
      <td data-category="A/O" class="pct share sep">5.5%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #8ac7e5">42.4%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f8806a">56.0%</div>
      </td>
    </tr>
    <tr data-state="Arkansas" class="state Arkansas">
      <td class="name">Ark.</td>
      <td class="ev sep">
        <div>6
        </div>
      </td>
      <td data-category="CEW" class="pct share">28.1%</td>
      <td data-category="NCEW" class="pct share">51.2%</td>
      <td data-category="Black" class="pct share">11.6%</td>
      <td data-category="Latino" class="pct share">4.7%</td>
      <td data-category="A/O" class="pct share sep">4.5%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #91cae5">39.5%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f97c65">58.0%</div>
      </td>
    </tr>
    <tr data-state="California" class="state California">
      <td class="name">Calif.</td>
      <td class="ev sep">
        <div>55
        </div>
      </td>
      <td data-category="CEW" class="pct share">22.8%</td>
      <td data-category="NCEW" class="pct share">24.7%</td>
      <td data-category="Black" class="pct share">6.9%</td>
      <td data-category="Latino" class="pct share">27.7%</td>
      <td data-category="A/O" class="pct share sep">18.0%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #7ac0e3">49.0%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f78f7c">48.4%</div>
      </td>
    </tr>
    <tr data-state="Colorado" class="state Colorado">
      <td class="name">Colo.</td>
      <td class="ev sep">
        <div>9
        </div>
      </td>
      <td data-category="CEW" class="pct share">32.4%</td>
      <td data-category="NCEW" class="pct share">38.1%</td>
      <td data-category="Black" class="pct share">2.6%</td>
      <td data-category="Latino" class="pct share">18.3%</td>
      <td data-category="A/O" class="pct share sep">8.7%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #78c0e3">49.8%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f7907d">47.8%</div>
      </td>
    </tr>
    <tr data-state="Connecticut" class="state Connecticut">
      <td class="name">Conn.</td>
      <td class="ev sep">
        <div>7
        </div>
      </td>
      <td data-category="CEW" class="pct share">43.5%</td>
      <td data-category="NCEW" class="pct share">30.7%</td>
      <td data-category="Black" class="pct share">11.8%</td>
      <td data-category="Latino" class="pct share">9.4%</td>
      <td data-category="A/O" class="pct share sep">4.5%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #66b8e1">57.4%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f69d8c">41.5%</div>
      </td>
    </tr>
    <tr data-state="Delaware" class="state Delaware">
      <td class="name">Del.</td>
      <td class="ev sep">
        <div>3
        </div>
      </td>
      <td data-category="CEW" class="pct share">34.0%</td>
      <td data-category="NCEW" class="pct share">38.7%</td>
      <td data-category="Black" class="pct share">17.7%</td>
      <td data-category="Latino" class="pct share">4.9%</td>
      <td data-category="A/O" class="pct share sep">4.7%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #79c0e3">49.7%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f78e7b">48.7%</div>
      </td>
    </tr>
    <tr data-state="District of Columbia" class="state District of Columbia">
      <td class="name">D.C.</td>
      <td class="ev sep">
        <div>3
        </div>
      </td>
      <td data-category="CEW" class="pct share">32.6%</td>
      <td data-category="NCEW" class="pct share">2.3%</td>
      <td data-category="Black" class="pct share">53.4%</td>
      <td data-category="Latino" class="pct share">8.6%</td>
      <td data-category="A/O" class="pct share sep">3.1%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #7ec2e3">47.5%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f88a76">50.7%</div>
      </td>
    </tr>
    <tr data-state="Florida" class="state Florida">
      <td class="name">Fla.</td>
      <td class="ev sep">
        <div>29
        </div>
      </td>
      <td data-category="CEW" class="pct share">26.3%</td>
      <td data-category="NCEW" class="pct share">33.1%</td>
      <td data-category="Black" class="pct share">12.2%</td>
      <td data-category="Latino" class="pct share">23.1%</td>
      <td data-category="A/O" class="pct share sep">5.3%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #8dc8e5">41.4%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f97c66">57.7%</div>
      </td>
    </tr>
    <tr data-state="Georgia" class="state Georgia">
      <td class="name">Ga.</td>
      <td class="ev sep">
        <div>16
        </div>
      </td>
      <td data-category="CEW" class="pct share">26.7%</td>
      <td data-category="NCEW" class="pct share">34.9%</td>
      <td data-category="Black" class="pct share">30.6%</td>
      <td data-category="Latino" class="pct share">4.4%</td>
      <td data-category="A/O" class="pct share sep">3.4%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #94cbe6">38.4%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f9765f">60.5%</div>
      </td>
    </tr>
    <tr data-state="Hawaii" class="state Hawaii">
      <td class="name">Hawaii</td>
      <td class="ev sep">
        <div>4
        </div>
      </td>
      <td data-category="CEW" class="pct share">15.4%</td>
      <td data-category="NCEW" class="pct share">19.2%</td>
      <td data-category="Black" class="pct share">1.2%</td>
      <td data-category="Latino" class="pct share">11.2%</td>
      <td data-category="A/O" class="pct share sep">53.0%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #49addd">69.4%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f4b6aa">29.0%</div>
      </td>
    </tr>
    <tr data-state="Idaho" class="state Idaho">
      <td class="name">Idaho</td>
      <td class="ev sep">
        <div>4
        </div>
      </td>
      <td data-category="CEW" class="pct share">25.6%</td>
      <td data-category="NCEW" class="pct share">60.1%</td>
      <td data-category="Black" class="pct share">1.3%</td>
      <td data-category="Latino" class="pct share">8.9%</td>
      <td data-category="A/O" class="pct share sep">4.0%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #9acde6">35.6%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f9745c">61.7%</div>
      </td>
    </tr>
    <tr data-state="Illinois" class="state Illinois">
      <td class="name">Ill.</td>
      <td class="ev sep">
        <div>20
        </div>
      </td>
      <td data-category="CEW" class="pct share">30.2%</td>
      <td data-category="NCEW" class="pct share">34.6%</td>
      <td data-category="Black" class="pct share">13.1%</td>
      <td data-category="Latino" class="pct share">16.4%</td>
      <td data-category="A/O" class="pct share sep">5.7%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #7ec2e3">47.4%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f88a76">51.0%</div>
      </td>
    </tr>
    <tr data-state="Indiana" class="state Indiana">
      <td class="name">Ind.</td>
      <td class="ev sep">
        <div>11
        </div>
      </td>
      <td data-category="CEW" class="pct share">35.1%</td>
      <td data-category="NCEW" class="pct share">45.6%</td>
      <td data-category="Black" class="pct share">7.9%</td>
      <td data-category="Latino" class="pct share">8.4%</td>
      <td data-category="A/O" class="pct share sep">3.0%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #80c3e3">46.7%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f88975">51.4%</div>
      </td>
    </tr>
    <tr data-state="Iowa" class="state Iowa">
      <td class="name">Iowa</td>
      <td class="ev sep">
        <div>6
        </div>
      </td>
      <td data-category="CEW" class="pct share">35.2%</td>
      <td data-category="NCEW" class="pct share">56.4%</td>
      <td data-category="Black" class="pct share">2.2%</td>
      <td data-category="Latino" class="pct share">3.0%</td>
      <td data-category="A/O" class="pct share sep">3.2%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #79c0e3">49.4%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f78e7b">48.8%</div>
      </td>
    </tr>
    <tr data-state="Kansas" class="state Kansas">
      <td class="name">Kan.</td>
      <td class="ev sep">
        <div>6
        </div>
      </td>
      <td data-category="CEW" class="pct share">36.1%</td>
      <td data-category="NCEW" class="pct share">47.5%</td>
      <td data-category="Black" class="pct share">4.9%</td>
      <td data-category="Latino" class="pct share">7.2%</td>
      <td data-category="A/O" class="pct share sep">4.3%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #7ec2e3">47.5%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f88b77">50.2%</div>
      </td>
    </tr>
    <tr data-state="Kentucky" class="state Kentucky">
      <td class="name">Ky.</td>
      <td class="ev sep">
        <div>8
        </div>
      </td>
      <td data-category="CEW" class="pct share">28.7%</td>
      <td data-category="NCEW" class="pct share">54.0%</td>
      <td data-category="Black" class="pct share">10.7%</td>
      <td data-category="Latino" class="pct share">3.4%</td>
      <td data-category="A/O" class="pct share sep">3.2%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #92cae5">39.4%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f97962">59.0%</div>
      </td>
    </tr>
    <tr data-state="Louisiana" class="state Louisiana">
      <td class="name">La.</td>
      <td class="ev sep">
        <div>8
        </div>
      </td>
      <td data-category="CEW" class="pct share">24.9%</td>
      <td data-category="NCEW" class="pct share">38.4%</td>
      <td data-category="Black" class="pct share">28.4%</td>
      <td data-category="Latino" class="pct share">6.8%</td>
      <td data-category="A/O" class="pct share sep">1.5%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #9ecfe7">34.3%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #fa6f56">64.1%</div>
      </td>
    </tr>
    <tr data-state="Maine" class="state Maine">
      <td class="name">Maine</td>
      <td class="ev sep">
        <div>4
        </div>
      </td>
      <td data-category="CEW" class="pct share">41.9%</td>
      <td data-category="NCEW" class="pct share">52.3%</td>
      <td data-category="Black" class="pct share">1.4%</td>
      <td data-category="Latino" class="pct share">1.6%</td>
      <td data-category="A/O" class="pct share sep">2.8%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #6dbbe1">54.6%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f69a8a">42.7%</div>
      </td>
    </tr>
    <tr data-state="Maryland" class="state Maryland">
      <td class="name">Md.</td>
      <td class="ev sep">
        <div>10
        </div>
      </td>
      <td data-category="CEW" class="pct share">30.3%</td>
      <td data-category="NCEW" class="pct share">22.9%</td>
      <td data-category="Black" class="pct share">27.7%</td>
      <td data-category="Latino" class="pct share">10.6%</td>
      <td data-category="A/O" class="pct share sep">8.5%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #7ec2e3">47.3%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f88a77">50.6%</div>
      </td>
    </tr>
    <tr data-state="Massachusetts" class="state Massachusetts">
      <td class="name">Mass.</td>
      <td class="ev sep">
        <div>11
        </div>
      </td>
      <td data-category="CEW" class="pct share">49.3%</td>
      <td data-category="NCEW" class="pct share">33.1%</td>
      <td data-category="Black" class="pct share">6.4%</td>
      <td data-category="Latino" class="pct share">6.4%</td>
      <td data-category="A/O" class="pct share sep">4.9%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #5ab4df">62.3%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f5a89a">35.8%</div>
      </td>
    </tr>
    <tr data-state="Michigan" class="state Michigan">
      <td class="name">Mich.</td>
      <td class="ev sep">
        <div>16
        </div>
      </td>
      <td data-category="CEW" class="pct share">33.5%</td>
      <td data-category="NCEW" class="pct share">41.2%</td>
      <td data-category="Black" class="pct share">15.1%</td>
      <td data-category="Latino" class="pct share">4.3%</td>
      <td data-category="A/O" class="pct share sep">6.0%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #7ac0e3">49.2%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f78c79">49.6%</div>
      </td>
    </tr>
    <tr data-state="Minnesota" class="state Minnesota">
      <td class="name">Minn.</td>
      <td class="ev sep">
        <div>10
        </div>
      </td>
      <td data-category="CEW" class="pct share">36.5%</td>
      <td data-category="NCEW" class="pct share">45.5%</td>
      <td data-category="Black" class="pct share">6.6%</td>
      <td data-category="Latino" class="pct share">4.2%</td>
      <td data-category="A/O" class="pct share sep">7.2%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #73bee2">52.0%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f79482">45.7%</div>
      </td>
    </tr>
    <tr data-state="Mississippi" class="state Mississippi">
      <td class="name">Miss.</td>
      <td class="ev sep">
        <div>6
        </div>
      </td>
      <td data-category="CEW" class="pct share">20.7%</td>
      <td data-category="NCEW" class="pct share">38.7%</td>
      <td data-category="Black" class="pct share">35.1%</td>
      <td data-category="Latino" class="pct share">4.0%</td>
      <td data-category="A/O" class="pct share sep">1.4%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #a7d2e8">30.5%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #fa664b">68.7%</div>
      </td>
    </tr>
    <tr data-state="Missouri" class="state Missouri">
      <td class="name">Mo.</td>
      <td class="ev sep">
        <div>10
        </div>
      </td>
      <td data-category="CEW" class="pct share">27.6%</td>
      <td data-category="NCEW" class="pct share">48.1%</td>
      <td data-category="Black" class="pct share">15.8%</td>
      <td data-category="Latino" class="pct share">4.3%</td>
      <td data-category="A/O" class="pct share sep">4.2%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #90c9e5">40.2%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f97b65">58.0%</div>
      </td>
    </tr>
    <tr data-state="Montana" class="state Montana">
      <td class="name">Mont.</td>
      <td class="ev sep">
        <div>3
        </div>
      </td>
      <td data-category="CEW" class="pct share">31.6%</td>
      <td data-category="NCEW" class="pct share">52.8%</td>
      <td data-category="Black" class="pct share">2.0%</td>
      <td data-category="Latino" class="pct share">6.0%</td>
      <td data-category="A/O" class="pct share sep">7.6%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #83c4e4">45.4%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f88874">51.7%</div>
      </td>
    </tr>
    <tr data-state="Nebraska" class="state Nebraska">
      <td class="name">Neb.</td>
      <td class="ev sep">
        <div>5
        </div>
      </td>
      <td data-category="CEW" class="pct share">35.4%</td>
      <td data-category="NCEW" class="pct share">53.8%</td>
      <td data-category="Black" class="pct share">4.4%</td>
      <td data-category="Latino" class="pct share">3.3%</td>
      <td data-category="A/O" class="pct share sep">3.1%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #83c4e4">45.5%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f88773">52.3%</div>
      </td>
    </tr>
    <tr data-state="Nevada" class="state Nevada">
      <td class="name">Nev.</td>
      <td class="ev sep">
        <div>6
        </div>
      </td>
      <td data-category="CEW" class="pct share">21.6%</td>
      <td data-category="NCEW" class="pct share">33.8%</td>
      <td data-category="Black" class="pct share">8.5%</td>
      <td data-category="Latino" class="pct share">24.3%</td>
      <td data-category="A/O" class="pct share sep">11.9%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #8ac7e4">42.6%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f8816b">55.2%</div>
      </td>
    </tr>
    <tr data-state="New Hampshire" class="state New Hampshire">
      <td class="name">N.H.</td>
      <td class="ev sep">
        <div>4
        </div>
      </td>
      <td data-category="CEW" class="pct share">41.1%</td>
      <td data-category="NCEW" class="pct share">49.0%</td>
      <td data-category="Black" class="pct share">2.2%</td>
      <td data-category="Latino" class="pct share">4.5%</td>
      <td data-category="A/O" class="pct share sep">3.2%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #70bce2">53.4%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f79684">45.0%</div>
      </td>
    </tr>
    <tr data-state="New Jersey" class="state New Jersey">
      <td class="name">N.J.</td>
      <td class="ev sep">
        <div>14
        </div>
      </td>
      <td data-category="CEW" class="pct share">27.4%</td>
      <td data-category="NCEW" class="pct share">33.9%</td>
      <td data-category="Black" class="pct share">17.4%</td>
      <td data-category="Latino" class="pct share">14.3%</td>
      <td data-category="A/O" class="pct share sep">6.9%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #84c4e4">45.0%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f8846f">53.9%</div>
      </td>
    </tr>
    <tr data-state="New Mexico" class="state New Mexico">
      <td class="name">N.M.</td>
      <td class="ev sep">
        <div>5
        </div>
      </td>
      <td data-category="CEW" class="pct share">17.7%</td>
      <td data-category="NCEW" class="pct share">23.6%</td>
      <td data-category="Black" class="pct share">1.7%</td>
      <td data-category="Latino" class="pct share">44.1%</td>
      <td data-category="A/O" class="pct share sep">12.9%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #91cae5">39.6%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f8806a">55.9%</div>
      </td>
    </tr>
    <tr data-state="New York" class="state New York">
      <td class="name">N.Y.</td>
      <td class="ev sep">
        <div>29
        </div>
      </td>
      <td data-category="CEW" class="pct share">31.6%</td>
      <td data-category="NCEW" class="pct share">30.5%</td>
      <td data-category="Black" class="pct share">15.4%</td>
      <td data-category="Latino" class="pct share">18.1%</td>
      <td data-category="A/O" class="pct share sep">4.3%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #7cc1e3">48.2%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f88a77">50.5%</div>
      </td>
    </tr>
    <tr data-state="North Carolina" class="state North Carolina">
      <td class="name">N.C.</td>
      <td class="ev sep">
        <div>15
        </div>
      </td>
      <td data-category="CEW" class="pct share">29.0%</td>
      <td data-category="NCEW" class="pct share">38.5%</td>
      <td data-category="Black" class="pct share">22.5%</td>
      <td data-category="Latino" class="pct share">5.7%</td>
      <td data-category="A/O" class="pct share sep">4.2%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #8ec8e5">41.0%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f97c66">57.7%</div>
      </td>
    </tr>
    <tr data-state="North Dakota" class="state North Dakota">
      <td class="name">N.D.</td>
      <td class="ev sep">
        <div>3
        </div>
      </td>
      <td data-category="CEW" class="pct share">35.9%</td>
      <td data-category="NCEW" class="pct share">51.8%</td>
      <td data-category="Black" class="pct share">2.1%</td>
      <td data-category="Latino" class="pct share">4.2%</td>
      <td data-category="A/O" class="pct share sep">6.0%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #7dc2e3">47.9%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f78d7a">49.1%</div>
      </td>
    </tr>
    <tr data-state="Ohio" class="state Ohio">
      <td class="name">Ohio</td>
      <td class="ev sep">
        <div>18
        </div>
      </td>
      <td data-category="CEW" class="pct share">30.2%</td>
      <td data-category="NCEW" class="pct share">46.3%</td>
      <td data-category="Black" class="pct share">14.5%</td>
      <td data-category="Latino" class="pct share">4.5%</td>
      <td data-category="A/O" class="pct share sep">4.6%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #85c5e4">44.8%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f8846f">53.6%</div>
      </td>
    </tr>
    <tr data-state="Oklahoma" class="state Oklahoma">
      <td class="name">Okla.</td>
      <td class="ev sep">
        <div>7
        </div>
      </td>
      <td data-category="CEW" class="pct share">27.1%</td>
      <td data-category="NCEW" class="pct share">50.4%</td>
      <td data-category="Black" class="pct share">6.9%</td>
      <td data-category="Latino" class="pct share">4.7%</td>
      <td data-category="A/O" class="pct share sep">10.9%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #87c5e4">43.8%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f87f69">56.1%</div>
      </td>
    </tr>
    <tr data-state="Oregon" class="state Oregon">
      <td class="name">Ore.</td>
      <td class="ev sep">
        <div>7
        </div>
      </td>
      <td data-category="CEW" class="pct share">36.7%</td>
      <td data-category="NCEW" class="pct share">46.9%</td>
      <td data-category="Black" class="pct share">1.0%</td>
      <td data-category="Latino" class="pct share">5.6%</td>
      <td data-category="A/O" class="pct share sep">9.8%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #70bce2">53.5%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f69a89">42.9%</div>
      </td>
    </tr>
    <tr data-state="Pennsylvania" class="state Pennsylvania">
      <td class="name">Pa.</td>
      <td class="ev sep">
        <div>20
        </div>
      </td>
      <td data-category="CEW" class="pct share">36.5%</td>
      <td data-category="NCEW" class="pct share">38.0%</td>
      <td data-category="Black" class="pct share">13.1%</td>
      <td data-category="Latino" class="pct share">9.3%</td>
      <td data-category="A/O" class="pct share sep">3.1%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #79c0e3">49.6%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f78e7b">48.9%</div>
      </td>
    </tr>
    <tr data-state="Rhode Island" class="state Rhode Island">
      <td class="name">R.I.</td>
      <td class="ev sep">
        <div>4
        </div>
      </td>
      <td data-category="CEW" class="pct share">33.1%</td>
      <td data-category="NCEW" class="pct share">43.1%</td>
      <td data-category="Black" class="pct share">7.0%</td>
      <td data-category="Latino" class="pct share">11.3%</td>
      <td data-category="A/O" class="pct share sep">5.6%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #77bfe2">50.4%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f7907d">47.7%</div>
      </td>
    </tr>
    <tr data-state="South Carolina" class="state South Carolina">
      <td class="name">S.C.</td>
      <td class="ev sep">
        <div>9
        </div>
      </td>
      <td data-category="CEW" class="pct share">31.2%</td>
      <td data-category="NCEW" class="pct share">38.7%</td>
      <td data-category="Black" class="pct share">23.7%</td>
      <td data-category="Latino" class="pct share">4.6%</td>
      <td data-category="A/O" class="pct share sep">1.8%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #8ec8e5">41.0%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f97c66">57.6%</div>
      </td>
    </tr>
    <tr data-state="South Dakota" class="state South Dakota">
      <td class="name">S.D.</td>
      <td class="ev sep">
        <div>3
        </div>
      </td>
      <td data-category="CEW" class="pct share">34.4%</td>
      <td data-category="NCEW" class="pct share">49.0%</td>
      <td data-category="Black" class="pct share">1.4%</td>
      <td data-category="Latino" class="pct share">5.7%</td>
      <td data-category="A/O" class="pct share sep">9.5%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #78c0e3">49.8%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f78f7d">48.0%</div>
      </td>
    </tr>
    <tr data-state="Tennessee" class="state Tennessee">
      <td class="name">Tenn.</td>
      <td class="ev sep">
        <div>11
        </div>
      </td>
      <td data-category="CEW" class="pct share">31.3%</td>
      <td data-category="NCEW" class="pct share">49.2%</td>
      <td data-category="Black" class="pct share">11.4%</td>
      <td data-category="Latino" class="pct share">3.1%</td>
      <td data-category="A/O" class="pct share sep">5.0%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #88c6e4">43.3%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f8816c">55.2%</div>
      </td>
    </tr>
    <tr data-state="Texas" class="state Texas">
      <td class="name">Texas</td>
      <td class="ev sep">
        <div>38
        </div>
      </td>
      <td data-category="CEW" class="pct share">26.7%</td>
      <td data-category="NCEW" class="pct share">27.8%</td>
      <td data-category="Black" class="pct share">12.3%</td>
      <td data-category="Latino" class="pct share">27.1%</td>
      <td data-category="A/O" class="pct share sep">6.1%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #8dc8e5">41.3%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f97d67">57.2%</div>
      </td>
    </tr>
    <tr data-state="Utah" class="state Utah">
      <td class="name">Utah</td>
      <td class="ev sep">
        <div>6
        </div>
      </td>
      <td data-category="CEW" class="pct share">33.6%</td>
      <td data-category="NCEW" class="pct share">52.1%</td>
      <td data-category="Black" class="pct share">1.2%</td>
      <td data-category="Latino" class="pct share">7.2%</td>
      <td data-category="A/O" class="pct share sep">5.9%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #87c5e4">43.9%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f8846f">53.7%</div>
      </td>
    </tr>
    <tr data-state="Vermont" class="state Vermont">
      <td class="name">Vt.</td>
      <td class="ev sep">
        <div>3
        </div>
      </td>
      <td data-category="CEW" class="pct share">41.9%</td>
      <td data-category="NCEW" class="pct share">48.6%</td>
      <td data-category="Black" class="pct share">0.9%</td>
      <td data-category="Latino" class="pct share">3.2%</td>
      <td data-category="A/O" class="pct share sep">5.4%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #66b8e0">57.4%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f69f90">40.2%</div>
      </td>
    </tr>
    <tr data-state="Virginia" class="state Virginia">
      <td class="name">Va.</td>
      <td class="ev sep">
        <div>13
        </div>
      </td>
      <td data-category="CEW" class="pct share">35.1%</td>
      <td data-category="NCEW" class="pct share">30.6%</td>
      <td data-category="Black" class="pct share">19.4%</td>
      <td data-category="Latino" class="pct share">7.3%</td>
      <td data-category="A/O" class="pct share sep">7.5%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #7ac0e3">49.2%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f78d7a">49.2%</div>
      </td>
    </tr>
    <tr data-state="Washington" class="state Washington">
      <td class="name">Wash.</td>
      <td class="ev sep">
        <div>12
        </div>
      </td>
      <td data-category="CEW" class="pct share">29.4%</td>
      <td data-category="NCEW" class="pct share">39.0%</td>
      <td data-category="Black" class="pct share">2.7%</td>
      <td data-category="Latino" class="pct share">13.7%</td>
      <td data-category="A/O" class="pct share sep">15.2%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #73bde2">52.2%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f79583">45.2%</div>
      </td>
    </tr>
    <tr data-state="West Virginia" class="state West Virginia">
      <td class="name">W.Va.</td>
      <td class="ev sep">
        <div>5
        </div>
      </td>
      <td data-category="CEW" class="pct share">28.4%</td>
      <td data-category="NCEW" class="pct share">62.3%</td>
      <td data-category="Black" class="pct share">2.2%</td>
      <td data-category="Latino" class="pct share">4.5%</td>
      <td data-category="A/O" class="pct share sep">2.5%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #92cae5">39.2%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f97a63">58.7%</div>
      </td>
    </tr>
    <tr data-state="Wisconsin" class="state Wisconsin">
      <td class="name">Wis.</td>
      <td class="ev sep">
        <div>10
        </div>
      </td>
      <td data-category="CEW" class="pct share">32.5%</td>
      <td data-category="NCEW" class="pct share">50.7%</td>
      <td data-category="Black" class="pct share">6.8%</td>
      <td data-category="Latino" class="pct share">5.7%</td>
      <td data-category="A/O" class="pct share sep">4.3%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #7ec2e3">47.4%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f88975">51.2%</div>
      </td>
    </tr>
    <tr data-state="Wyoming" class="state Wyoming">
      <td class="name">Wyo.</td>
      <td class="ev sep">
        <div>3
        </div>
      </td>
      <td data-category="CEW" class="pct share">33.3%</td>
      <td data-category="NCEW" class="pct share">53.4%</td>
      <td data-category="Black" class="pct share">1.4%</td>
      <td data-category="Latino" class="pct share">7.7%</td>
      <td data-category="A/O" class="pct share sep">4.2%</td>
      <td data-party="D" class="party-vote">
        <div style="background-color: #8fc9e5">40.6%</div>
      </td>
      <td data-party="R" class="party-vote">
        <div style="background-color: #f8806a">55.9%</div>
      </td>
    </tr>
  </tbody>
</table>
 """

soup = BeautifulSoup(html)
table = soup.find("table")

# The first tr contains the field names.
headings = [th.get_text() for th in table.find("tr").find_all("th")]

datasets = []
for row in table.find_all("tr")[1:]:
    dataset = [td.get_text() for td in row.find_all("td")]
    datasets.append(dataset)

#print datasets

for field in headings:
    print field+"\t",
print
for dataset in datasets:
    print
    for field in dataset:
        print field.strip().strip(" %")+"\t",

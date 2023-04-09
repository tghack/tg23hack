> Author: NorskFjellGeit#9620

## Chall
### Description
    Scrooge McDuck's money is at the Duckburg Bank.

    Can you manage to steal everything?

    Link: ``duckburgbank.chall.tghack.no``


### Solution

First: The Login

The login page is badly written. Open the source code of the html, and then you will see that the javascript 
actually contains Scrooge's password in base64 in the javascript. Decode with base64 and voila, the flag.

Flag: `TG23{everything_in_the_bank_is_mine}`

Second: The Cookie
You are now logged in and can see Scrooge's account balance. But you do not have any rights to do anything banking actions.
Check to see if there are any cookies that can give you more privileges. Set IS_ADMIN='true', and reopen the account page. 
You are then able to withdraw the money.  Click it, and voila!

Flag: `TG23{now_i_want_to_take_everything_with_me}`

Third: The Stego
When you withdraw the money, you get a check image. This image has an embedded image with the flag. Run it through CyberChef ex. with the `Extract Files` recipe. And voila, you see there are two png's in one file. The second one contains the flag.

Flag: `TG23{this_is_the_most_valuable_file_in_duckburg}`


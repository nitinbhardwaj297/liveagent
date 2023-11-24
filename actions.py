# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import requests
from typing import Any, Text, Dict, List
import os, requests
import time
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, UserUttered, ActionExecuted, Restarted
from actions import langchain_qa


class ActionRestart(Action):
    def name(self):
        return "action_restart"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]


class ChatGPT(object):
    def __init__(self, api_key):
        self.url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-3.5-turbo"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    def ask(self, question):
        body = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful bot."},
                {"role": "user", "content": question},
            ],
        }
        result = requests.post(
            url=self.url,
            headers=self.headers,
            json=body,
        )

        if result.status_code == 200:
            chatgpt_response = result.json()
            return chatgpt_response["choices"][0]["message"]["content"]
        else:
            return "Sorry, I couldn't generate a response at the moment. Please try again later."


chatGPT = ChatGPT("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")


class ActionResetProductSlot(Action):
    def name(self) -> Text:
        return "action_reset_product_slot"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("product_category", None), SlotSet("product_name", None)]


class ActionResetPreviousContraceptionSlot(Action):
    def name(self) -> Text:
        return "action_reset_previous_contraception_slot"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        return [
            SlotSet("previous_contraception_method", None),
            SlotSet("previous_contraception_satisfaction", None),
        ]


class ActionResetDisconReqReasonSlot(Action):
    def name(self) -> Text:
        return "action_reset_discon_req_reason_slot"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("discon_req_reason", None)]


class ActionIntro(Action):
    def name(self) -> Text:
        return "action_intro"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        start_intent = tracker.events[3]["parse_data"]["intent"]["name"]

        return (
            [SlotSet("conv_start", True)]
            + [ActionExecuted("action_listen")]
            + [
                UserUttered(
                    tracker.events[3]["text"],
                    {
                        "intent": {
                            "name": tracker.events[3]["parse_data"]["intent"]["name"],
                            "confidence": 1.0,
                        },
                        "entities": [],
                    },
                )
            ]
        )
        # return [SlotSet('discon_req_reason', None)]


class ActionAskGPT(Action):
    def name(self) -> Text:
        return "action_ask_gpt"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        last_intent = tracker.latest_message["intent"]["name"]
        if last_intent == "nlu_fallback":
            question = tracker.latest_message["text"]
        else:
            question = tracker.get_slot("gpt_question")
        # answer = chatGPT.ask(question)
        print(question)
        answer="OpenAI tokens limit reached"
        #answer = langchain_qa.get_answer(question)
        print("answer", answer)
        dispatcher.utter_message(text=answer)
        time.sleep(2)
        dispatcher.utter_message(
            text="Would you like to continue?\nPlease type 'Yes' to proceed, or type 'stop' to exit."
        )

        return [SlotSet("gpt_question", None)]


class ActionHandleVideoRequest(Action):
    def name(self) -> Text:
        return "action_penegra_audio"

    def send_audio_to_telegram(self, chat_id: Text, audio_path: Text) -> None:
        bot_token = "6415620982:AAEe2yw_dkmzdOdieCq9OQSfjZ0587Y0VLo"
        api_url = f"https://api.telegram.org/bot{bot_token}/sendAudio"
        params = {"chat_id": chat_id}
        files = {"audio": (audio_path, open(audio_path, "rb"))}
        response = requests.post(api_url, params=params, files=files)
        self.check_response_status(response, "Audio")

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        chat_id = tracker.sender_id

        audio_path = "Penegra.mp3"
        self.send_audio_to_telegram(chat_id, audio_path)

        # video_path = "video.mp4"
        # self.send_video_to_telegram(chat_id, video_path)

        #dispatcher.utter_message(text="Sure! I'll send you an audio shortly.")

        # latitude = 26.850000
        # longitude = 80.949997
        # self.send_location_to_telegram(chat_id, latitude, longitude)

        # latitude = 37.7749
        # longitude = -122.4194
        # title = "Example Venue"
        # address = "123 Main Street, Cityville"
        # self.send_venue_to_telegram(chat_id, latitude, longitude, title, address)

        # phone_number = "7790"
        # self.send_phone_number_to_telegram(chat_id, phone_number)

        # dispatcher.utter_message(
        # text="Sure! I'll send you the requested information shortly."
        # )

        return []


class Progesta_audio_send(Action):
    def name(self) -> Text:
        return "action_Progesta_audio"

    def send_audio_to_telegram(self, chat_id: Text, audio_path: Text) -> None:
        bot_token = "6415620982:AAEe2yw_dkmzdOdieCq9OQSfjZ0587Y0VLo"
        api_url = f"https://api.telegram.org/bot{bot_token}/sendAudio"
        params = {"chat_id": chat_id}
        files = {"audio": (audio_path, open(audio_path, "rb"))}
        response = requests.post(api_url, params=params, files=files)
        self.check_response_status(response, "Audio")

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        chat_id = tracker.sender_id
        audio_path = "progesta.mp3"
        self.send_audio_to_telegram(chat_id, audio_path)
        # Extract the payload from the user's latest message
        # selected_intent = tracker.latest_message["payload"]
        ##try:
        ##dispatcher.utter_message(
        ##text="I can refer you to a clinic if you would like to adopt this method"
        ##)
        # latest_message = tracker.latest_message
        # selected_intent = latest_message["intent"]["name"]
        ##except:
        ##pass

        """try:
            # Perform different actions based on the selected button
            if selected_intent == "Contraceptive_Injectables_Progesta":
                # dispatcher.utter_message(
                # image="https://s3.typebot.io/public/workspaces/clmis6ucm000il50gyvzllels/typebots/clmis9a0q000ol50gdavazp8y/blocks/fwty6spob6fvmzy7d6kigsbv?v=1699596361639"
                # )

                # dispatcher.utter_message(
                # text="Progesta is an injectable contraceptive,highly safe and effective contraceptive,injected intramuscular and sometimes into the anus for 3months continuous.\nMechanism of Action\n• thicken cervical mucus.\n• inhibits ovulation.\n• thins uterus walls to prevent ovulation.\nAdvantages include Safe, highly effective, discontinued at will, long acting, provided outside clinic, reversible, easy to use, use is private, non-contraceptive benefit.\nUsers include heavy smokers, thyroid disorders, diabetes, 18yrs old or younger, breastfeeding mothers, pelvic inflammatory diseases.\n\nHow to use\n• Injected in the upper arm or buttocks, start at any time during the menstrual cycle.\n• 5 days after menstrual period, abstain from sex for the next 7days.\n• It can be administered after abortion.\n• Start 6 weeks after delivery for a breastfeeding woman\n\nYou can click on the audio below to listen to a short introduction of Progesta in pidgin, if you want to."
                # )

                audio_path = "progesta.mp3"
                self.send_audio_to_telegram(chat_id, audio_path)

                dispatcher.utter_message(
                    text="I can refer you to a clinic if you would like to adopt this method"
                )

                # Add specific logic for Postpill
            elif selected_intent == "Contraceptive_Injectables_Sayana_Press":
                dispatcher.utter_message(
                    text="Here are some of the side effects associated with emergency contraceptives\n\n1. Mild headache.2. Nausea or vomiting.\n3. Dizziness\n4. Breast tenderness.\n5. Lower abdominal discomfort.\n6. Menstrual change (period may come early)\n\nThey usually goes away after some days.\n\nAre you experiencing any of these side effects?"
                )
            else:
                dispatcher.utter_message(text="Invalid selection. Please try again.")
        except:
            pass"""

        return []


class Sayana_Press_audio_send(Action):
    def name(self) -> Text:
        return "action_Sayana_Press_audio"

    def send_audio_to_telegram(self, chat_id: Text, audio_path: Text) -> None:
        bot_token = "6415620982:AAEe2yw_dkmzdOdieCq9OQSfjZ0587Y0VLo"
        api_url = f"https://api.telegram.org/bot{bot_token}/sendAudio"
        params = {"chat_id": chat_id}
        files = {"audio": (audio_path, open(audio_path, "rb"))}
        response = requests.post(api_url, params=params, files=files)
        self.check_response_status(response, "Audio")

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        chat_id = tracker.sender_id
        audio_path = "SayanaPress.mp3"
        self.send_audio_to_telegram(chat_id, audio_path)

        return []

package io.yashxd.esdlab1;


import android.content.Context;
import android.util.Log;
import android.widget.Toast;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.DisconnectedBufferOptions;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;


public class MQTTHelper {
    public MqttAndroidClient mqttAndroidClient;

    private final String serverUri = "tcp://farmer.cloudmqtt.com:16881";

    private final String clientId = "ExampleAndroidClient";
    private final String subscriptionTopic = "lazybox/currentval";
    private final String publishingTopic = "lazybox/switchstate";

    private final String username = "juqupxax";
    private final String password = " 5PJgcg7EUX2V";

    private final String TAG = "MQTTHelper";

    private Context context;

    public MQTTHelper(Context context){
        mqttAndroidClient = new MqttAndroidClient(context, serverUri, clientId);
        mqttAndroidClient.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean b, String s) {
                Log.w(TAG, s);
            }

            @Override
            public void connectionLost(Throwable throwable) {
                //Issue here
                //Try to reconnect
            }

            @Override
            public void messageArrived(String topic, MqttMessage mqttMessage) throws Exception {
                Log.w(TAG, mqttMessage.toString());
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {
                //Lite.
            }
        });
        connect();
        this.context = context;
    }

    public void setCallback(MqttCallbackExtended callback) {
        mqttAndroidClient.setCallback(callback);
    }

    private void connect(){
        MqttConnectOptions mqttConnectOptions = new MqttConnectOptions();
        mqttConnectOptions.setAutomaticReconnect(true);
        mqttConnectOptions.setCleanSession(false);
        mqttConnectOptions.setUserName(username);
        mqttConnectOptions.setPassword(password.toCharArray());

        try {
            mqttAndroidClient.connect(mqttConnectOptions, null, new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {

                    DisconnectedBufferOptions disconnectedBufferOptions = new DisconnectedBufferOptions();
                    disconnectedBufferOptions.setBufferEnabled(true);
                    disconnectedBufferOptions.setBufferSize(100);
                    disconnectedBufferOptions.setPersistBuffer(false);
                    disconnectedBufferOptions.setDeleteOldestMessages(false);
                    mqttAndroidClient.setBufferOpts(disconnectedBufferOptions);

                    Toast.makeText(context, "Connected to MQTT Server", Toast.LENGTH_SHORT).show();
                    Log.d(TAG, "Connected to MQTT Server");
                    subscribeToTopic();
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    Log.w(TAG, "Failed to connect to: " + serverUri + exception.toString());
                }
            });


        } catch (MqttException ex){
            ex.printStackTrace();
            Log.e(TAG,ex.getMessage());
        }
    }


    private void subscribeToTopic() {
        try {
            mqttAndroidClient.subscribe(subscriptionTopic, 0, null, new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    Log.d(TAG,"Subscribed!");
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    Log.d(TAG, "Subscribed fail!");
                }
            });

        } catch (MqttException ex) {
            System.err.println("Exception whilst subscribing");
            ex.printStackTrace();
        }
    }
    public void publishMessage(String payload) throws MqttException {
        MqttMessage message = new MqttMessage(payload.getBytes());
        message.setQos(1);
        message.setRetained(true);
        mqttAndroidClient.publish(publishingTopic, message);
        Log.d(TAG, "Message Published");
    }

    public void disconnect() throws MqttException {
        mqttAndroidClient.disconnect();
        Log.d(TAG, "Disconnected Successfully");
    }
}


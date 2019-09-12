package io.yashxd.esdlab1;

public class DataItem {
    private int temp;
    private int light;
    private String timeStamp;

    public DataItem(int temp, int light, String timeStamp) {
        this.temp = temp;
        this.light = light;
        this.timeStamp = timeStamp;
    }

    public DataItem() {
        temp = 0;
        light = 0;
        timeStamp = "timeX";
    }

    public DataItem(DataItem dataItem) {
        this.temp = dataItem.getTemp();
        this.light = dataItem.getLight();
        this.timeStamp = dataItem.getTimeStamp();
    }

    public String getTimeStamp() {
        return timeStamp;
    }

    public void setTimeStamp(String timeStamp) {
        this.timeStamp = timeStamp;
    }

    public int getTemp() {
        return temp;
    }

    public void setTemp(int temp) {
        this.temp = temp;
    }

    public int getLight() {
        return light;
    }

    public void setLight(int light) {
        this.light = light;
    }
}

using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.Windows.Speech;
using UnityEngine.SceneManagement;
using KartGame.UI;

public class VoiceStartSolo : MonoBehaviour
{
    private KeywordRecognizer keywordRecognizer;
    private Dictionary<string, Action> actions = new Dictionary<string, Action>();

    void Start()
    {
        // actions.Add("forward", Forward);
        // actions.Add("up", Up);
        // actions.Add("down", Down);
        // actions.Add("back", Back);
        actions.Add("Solo", Begin);

        keywordRecognizer = new KeywordRecognizer(actions.Keys.ToArray());
        keywordRecognizer.OnPhraseRecognized += RecognizedSpeech;
        keywordRecognizer.Start();
        //keywordRecognizer.Stop;
    }

    private void RecognizedSpeech(PhraseRecognizedEventArgs speech)
    {
        Debug.Log(speech.text);
        actions[speech.text].Invoke();
    }

    // private void Forward()
    // {
    //     transform.Translate(-5, 0, 0);
    // }

    // private void Up()
    // {
    //     transform.Translate(0, 1, 0);
    // }

    // private void Back()
    // {
    //     transform.Translate(5, 0, 0);
    // }

    // private void Down()
    // {
    //     transform.Translate(0, -1, 0);
    // }


    // public KartGame.UI.LoadSceneButton other;
    // other.SceneName = "MainScene";
    private void Begin()
    {
        // other.LoadTargetScene();
        SceneManager.LoadScene("MainScene", LoadSceneMode.Single);
    }
}
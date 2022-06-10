using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.Windows.Speech;
using UnityEngine.SceneManagement;
using KartGame.UI;

public class VoiceWinMenu : MonoBehaviour
{
    private KeywordRecognizer keywordRecognizer;
    private Dictionary<string, Action> actions = new Dictionary<string, Action>();

    void Start()
    {
        actions.Add("reset", Menu);

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



    // public KartGame.UI.LoadSceneButton other;
    // other.SceneName = "MainScene";
    private void Menu()
    {
        // other.LoadTargetScene();
        SceneManager.LoadScene("IntroMenu",  LoadSceneMode.Single);
    }
}